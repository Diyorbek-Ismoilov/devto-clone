from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, RegisterForm
from .models import Post, Tag


def save_tags(post, names):
    post.tags.clear()
    for name in names:
        tag = Tag.objects.filter(name__iexact=name).first()
        if tag is None:
            tag = Tag.objects.create(name=name)
        post.tags.add(tag)


def post_list(request):
    posts = (
        Post.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related("tags")
    )
    return render(request, "blogapp/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not post.is_published and post.author != request.user:
        raise Http404

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.path)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blogapp:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    comments = post.comments.select_related("author")
    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blogapp/post_detail.html", context)


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = (
        tag.posts.filter(is_published=True)
        .select_related("author")
        .prefetch_related("tags")
    )
    return render(request, "blogapp/tag_posts.html", {"tag": tag, "posts": posts})


def register(request):
    if request.user.is_authenticated:
        return redirect("blogapp:post_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blogapp:post_list")
    else:
        form = RegisterForm()

    return render(request, "blogapp/register.html", {"form": form})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            save_tags(post, form.cleaned_data["tags"])
            return redirect("blogapp:post_detail", slug=post.slug)
    else:
        form = PostForm()

    return render(request, "blogapp/post_create.html", {"form": form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            save_tags(post, form.cleaned_data["tags"])
            return redirect("blogapp:post_detail", slug=post.slug)
    else:
        tag_names = ", ".join(tag.name for tag in post.tags.all())
        form = PostForm(instance=post, initial={"tags": tag_names})

    return render(request, "blogapp/post_create.html", {"form": form, "post": post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("blogapp:post_list")

    return render(request, "blogapp/post_confirm_delete.html", {"post": post})