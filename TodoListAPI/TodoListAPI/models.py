from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Todos(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
