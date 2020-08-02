from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField(
        "self", related_name="followers", blank=True, symmetrical=False
    )


class Post(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="likes")
