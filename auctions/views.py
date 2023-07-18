from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse
import re
from django.conf import settings
import os
from django.contrib import messages



from .utils import send_otp,generate_otp,send_confirmation,check_email_exists
from .models import User,Category,Course,History,Comment,Material

generated_otp=0
def index(request):
    courses=Course.objects.all()
    categories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "courses":courses,
        "categories":categories
    })

def filterCategory(request):
    if request.method=='POST':
        selCategory=request.POST['category']
        print(selCategory)
        categories=Category.objects.all()
        if selCategory not in categories.values_list("name",flat=True):
            return render(request,"auctions/error.html")
        else:
            cat=Category.objects.get(name=selCategory)
            filteredCourse=Course.objects.filter(category=cat)
        
            print (list(categories))
            return render(request,"auctions/index.html",{
                "courses":filteredCourse,
                "categories":categories
                })
    else:
        courses=Course.objects.filter(isActive=True)
        categories=Category.objects.all()
        return render(request, "auctions/index.html",{
            "courses":courses,
            "categories":categories
    })

def course(request,id):
    selCourse=Course.objects.get(pk=id)
    message=messages.get_messages(request)
    bought=request.user in selCourse.boughtBy.all()
    iswatching=request.user in selCourse.watchlist.all()
    comments=Comment.objects.filter(course=selCourse)
    material=Material.objects.filter(course=selCourse)
    return render(request,"auctions/course.html",{
        "course":selCourse,
        "iswatching":iswatching,
        "message":message,
        "bought":bought,
        "comments":comments,
        "material":material
    })

def download_material(request,topic_name):
    material=Material.objects.get(topic=topic_name)
    file_path=os.path.join(settings.MEDIA_ROOT,str(material.resource))
    print(file_path)
    with open(file_path,"rb") as f:
        response=HttpResponse(f.read(),content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(material.resource.name)

    return response
    
def add(request,id):
    selCourse=Course.objects.get(pk=id)
    curruser=request.user
    selCourse.watchlist.add(curruser)
    return HttpResponseRedirect(reverse("course", args=(id, )))

def remove(request,id):
    selCourse=Course.objects.get(pk=id)
    curruser=request.user
    selCourse.watchlist.remove(curruser)
    return HttpResponseRedirect(reverse("course", args=(id, )))

def watchlist(request):
    curruser=request.user
    categories=Category.objects.all()
    selCourse=curruser.watching.all()
    return render(request,"auctions/watchlist.html",{
        "courses":selCourse,
        "categories":categories
    }) 

def checkout(request,id):
    selCourse=Course.objects.get(pk=id)

    return render(request,"auctions/payment.html",{
        "course":selCourse
    })

def payment(request,id):
    selCourse=Course.objects.get(pk=id)
    curruser=request.user   
    if curruser.cash >= selCourse.price:
        curruser.cash -= selCourse.price
        curruser.save()
        selCourse.boughtBy.add(curruser)
        history=History(user=curruser,course=selCourse)
        send_confirmation(curruser.email,selCourse.title)
        history.save()
        messages.success(request,"Bought Successfully")
        return HttpResponseRedirect(reverse("course",args=(id, )))
    else:
        messages.warning(request,"Buy failed due to insufficient funds")
        return HttpResponseRedirect(reverse("course",args=(id,)))


def history(request):
    curruser = request.user
    history = History.objects.filter(user=curruser)
    categories=Category.objects.all()
    courses = [h.course for h in history]
    return render(request, "auctions/history.html", {
        "courses": courses,
        "categories":categories
    })

def addComment(request,id):
    curruser=request.user
    selCourse=Course.objects.get(pk=id)
    message=request.POST['newComment']

    comment=Comment(author=curruser,course=selCourse,message=message)

    comment.save()
    return HttpResponseRedirect(reverse('course',args=(id, )))

def profile(request):
    curruser=request.user
    return render(request,"auctions/profile.html",{
        "user":curruser
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
    
        if(check_email_exists(email)):
            request.session['username']=username
            request.session['email']=email
            request.session['password']=password
            global generated_otp 
            generated_otp= generate_otp()
            print("Otp generated",generated_otp)
            send_otp(email,generated_otp)
            return HttpResponseRedirect(reverse("verify"))
        else:
            return render(request, "auctions/register.html",{
                "message":"Email is not valid"
            })
    else:
        return render(request,"auctions/register.html")


def verify(request):
    if request.method=="POST":
        print("Verify generated otp",generated_otp)
        print(type(generated_otp))
        received_otp=int(request.POST['otp_field'])
        print("Recieved otp",received_otp)
        print(type(received_otp))
        username=request.session['username']
        email=request.session['email']
        password=request.session['password']

        if received_otp==generated_otp:
            print("creating user")
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "auctions/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/verify.html",{
                "message":"Otp invalid"
            })
    else:
        return render(request,"auctions/verify.html")
