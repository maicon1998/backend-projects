from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.redirect, name="redirect"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("home", views.home, name="home"),
    path("article/<int:id>", views.article, name="article"),
    path("admin", views.admin, name="admin"),
    path("new", views.new, name="new"),
    path("edit/<int:id>", views.edit, name="edit"),
]
