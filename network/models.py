from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import urlize, linebreaks


class User(AbstractUser):
    follows = models.ManyToManyField(
        "self", related_name="followers", blank=True, symmetrical=False
    )


class Post(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="likes", blank=True)

    def num_liked(self):
        return len(self.liked.all())

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": linebreaks(naturaltime(self.timestamp)),
            "liked": self.num_liked(),
            "users_liked": [user.id for user in self.liked.all()]
        }
