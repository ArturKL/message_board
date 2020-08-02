from django.contrib import admin
from .models import User, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "body", "timestamp", "likes_count")
    filter_horizontal = ("liked",)

    def likes_count(self, obj):
        return obj.liked.all().count()


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "follows_count", "followers_count")
    filter_horizontal = ("follows",)

    def follows_count(self, obj):
        return obj.follows.all().count()

    def followers_count(self, obj):
        return obj.followers.all().count()


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
