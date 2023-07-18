from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import get_upload_path


class User(AbstractUser):
    cash= models.IntegerField(default=10000,blank=True,null=True)

class Category(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=200)
    imageurl=models.CharField(max_length=200)
    price=models.IntegerField(max_length=20)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,related_name="category")
    watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="watching")
    boughtBy=models.ManyToManyField(User,blank=True,null=True,related_name="bought")
    
    def __str__(self):
        return f"{self.title}: {self.price}"
class History(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True, related_name="paid")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,related_name="sold")
    def __str__(self):
        return f"{self.user} bought {self.course}"

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True,related_name="commentCourse")
    message=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"

class Material(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, blank=True,null=True,related_name="material")
    topic=models.CharField(max_length=64)
    resource=models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return f"{self.course}: {self.topic} material {self.resource}"

    
    
    