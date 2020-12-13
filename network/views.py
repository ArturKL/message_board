from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

from django.core.exceptions import ObjectDoesNotExist

import json


from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
        forbidden = '*/\\'
        if any(symbol in username for symbol in forbidden):
            return render(
                request, "network/register.html", {"message": "Username should not contain *, \\, /"}
            )

        email = request.POST["email"]
        if not email:
            return render(
                request, "network/register.html", {"message": "Email is required"}
            )

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

        # Check if body length is valid adn save post
        if len(body) <= 300:
            post = Post()
            post.body = body
            post.author = request.user
            post.save()

        return HttpResponseRedirect(reverse("index"))


def profile(request, name):
    users = User.objects.annotate(num_followers=Count("followers"))
    try:
        user = users.get(username=name)
    except ObjectDoesNotExist:
        return render(request, 'network/error.html', {"status": 404, "message": 'User not found'})
    return render(request, "network/profile.html", {"user": user})


@login_required
def follow(request, name):
    user = User.objects.get(username=name)

    if user == request.user:
        return render(request, 'network/error.html', {"status": 404, "message": 'User not found'})

    if user in request.user.follows.all():
        request.user.follows.remove(user)
    elif user not in request.user.follows.all():
        request.user.follows.add(user)
    return HttpResponseRedirect(reverse(profile, args=[user.username]))


@login_required
def following_view(request):
    return render(request, 'network/following.html')


def posts(request, page_num, username):
    if username == '*':
        post_list = Post.objects\
                .order_by('-timestamp')
    elif username == '**':
        following = request.user.follows.all()
        post_list = Post.objects.filter(author__in=following)\
                .order_by('-timestamp')
    else:
        author = User.objects.get(username=username)
        post_list = Post.objects.filter(author=author).all()\
                .order_by('-timestamp')
    p = Paginator(post_list, 10)
    page = p.page(page_num)
    return JsonResponse([post.serialize() for post in page.object_list] + [{"num_pages": p.num_pages}], safe=False)


def get_post_by_id(request, id):
    try:
        post = Post.objects.get(pk=id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Post not found"}, status=404)
    return JsonResponse(post.serialize())


@login_required
def edit_post(request, post_id):
    if request.method != 'PUT':
        return JsonResponse({"message": "Request method invalid"})
    post = Post.objects.get(pk=post_id)
    if post.author == request.user:
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
            post.save()
            return HttpResponse(status=204)


@login_required
def like_post(request, id):
    if request.method == "PUT":
        post = Post.objects.get(pk=id)
        user = request.user
        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        post.save()
        return HttpResponse(status=204)

