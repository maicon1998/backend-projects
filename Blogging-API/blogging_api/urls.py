from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.create_read, name="create_read"),
    path("posts/<int:id>", views.read_update_delete, name="read_update_delete"),
]
