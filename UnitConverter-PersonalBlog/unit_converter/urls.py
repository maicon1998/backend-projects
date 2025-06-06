from django.urls import path
from . import views

app_name = "unit_converter"
urlpatterns = [
    path("", views.redirect, name="redirect"),
    path("length", views.length, name="length"),
    path("weight", views.weight, name="weight"),
    path("temperature", views.temperature, name="temperature"),
]
