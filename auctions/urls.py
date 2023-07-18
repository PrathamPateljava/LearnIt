from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category",views.filterCategory,name="category"),
    path("course/<int:id>",views.course,name="course"),
    path("remove/<int:id>",views.remove,name="remove"),
    path("add/<int:id>",views.add,name="add"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("history",views.history,name="history"),
    path("addComment/<int:id>",views.addComment,name="addComment"),
    path("profile",views.profile,name="profile"),
    path("download/<str:topic_name>/",views.download_material,name="download_material"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("verify",views.verify,name="verify"),
    path("checkout/<int:id>",views.checkout,name="checkout"),
    path("payment/<int:id>",views.payment,name="payment")
]
