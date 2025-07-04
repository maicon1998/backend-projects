from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("todos", views.todos_create_read, name="todos_create_read"),
    path("todos/<int:id>", views.todos_update_delete, name="todos_update_delete"),
]
