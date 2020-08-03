from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import User, Post


def index(request):
    posts = Post.objects.annotate(num_liked=Count("liked")).order_by('-timestamp')
    return render(request, "network/index.html", {"posts": posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        body = request.POST["body"]

        # Check if body lenght is valid adn save post
        if len(body) <= 300:
            post = Post()
            post.body = body
            post.author = request.user
            post.save()

        return HttpResponseRedirect(reverse("index"))


def profile(request, name):
    users = User.objects.annotate(num_followers=Count("followers"))
    user = users.get(username=name)

    # TODO: error page
    if not user:
        return HttpResponse("error")

    posts = Post.objects.filter(author=user).all().annotate(num_liked=Count("liked")).order_by('-timestamp')
    return render(request, "network/profile.html", {"user": user, "posts": posts})


@login_required
def follow(request, name):
    user = User.objects.get(username=name)
    # TODO: error page

    if user == request.user:
        return HttpResponse("error")

    if user in request.user.follows.all():
        request.user.follows.remove(user)
    elif user not in request.user.follows.all():
        request.user.follows.add(user)
    return HttpResponseRedirect(reverse(profile, args=[user.username]))


@login_required
def following_view(request):
    following = request.user.follows.all()
    posts = Post.objects.filter(author__in=following).annotate(num_liked=Count('liked')).order_by('-timestamp')
    return render(request, 'network/following.html', {"posts": posts})

