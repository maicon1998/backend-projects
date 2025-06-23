from django.db import models
from taggit.managers import TaggableManager


class Posts(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    tags = TaggableManager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
