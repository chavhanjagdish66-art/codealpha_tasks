from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post,Comment,Profile


@login_required
def home(request):
    if request.method=="POST":
        content=request.POST.get("content")
        image=request.FILES.get("image")
        Post.objects.create(author=request.user,content=content,image=image)
        return redirect("home")

    posts=Post.objects.all().order_by("-id")
    return render(request,"home.html",{"posts":posts})


@login_required
def like(request,id):
    post=get_object_or_404(Post,id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("home")


@login_required
def comment(request,id):
    post=get_object_or_404(Post,id=id)
    text=request.POST.get("text")
    Comment.objects.create(post=post,user=request.user,text=text)
    return redirect("home")


@login_required
def follow(request, username):
    target = get_object_or_404(User, username=username)

    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    target_profile, _ = Profile.objects.get_or_create(user=target)

    if target in my_profile.following.all():
        my_profile.following.remove(target)
        target_profile.followers.remove(request.user)
    else:
        my_profile.following.add(target)
        target_profile.followers.add(request.user)

    return redirect("profile", username=username)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    posts = Post.objects.filter(author=user)

    is_following = False
    if request.user != user:
        my_profile, _ = Profile.objects.get_or_create(user=request.user)
        if user in my_profile.following.all():
            is_following = True

    return render(request, "profile.html", {
        "profile_user": user,
        "profile": profile,
        "posts": posts,
        "is_following": is_following
    })