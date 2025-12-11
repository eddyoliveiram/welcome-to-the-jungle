from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm, CommentForm


def index(request):
    posts = Post.objects.select_related('author').prefetch_related('comments__author').order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'index.html', {'posts': posts, 'comment_form': comment_form})


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'profile.html', {'posts': posts})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('You can only edit your own posts')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden('You can only delete your own posts')
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'post_confirm_delete.html', {'post': post})


@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('index')
    return redirect('index')


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden('You can only edit your own comments')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_form.html', {'form': form, 'comment': comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden('You can only delete your own comments')
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('index')
    return render(request, 'comment_confirm_delete.html', {'comment': comment})
