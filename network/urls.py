from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path("u/<str:name>", views.profile, name="profile"),
    path("u/<str:name>/follow", views.follow, name="follow"),
    path("following", views.following_view, name="following"),
    path('posts/<int:page_num>/<str:username>', views.posts, name='posts')
]
