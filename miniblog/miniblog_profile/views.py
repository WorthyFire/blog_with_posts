import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files import File

from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm, RegistrationForm, PostForm, CommentForm
from .models import UserProfile, Post, Comment


def index(request):
    posts = Post.objects.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post_id = request.POST.get('post_id')
            new_comment.save()

    return render(request, 'index.html', {'posts': posts, 'comment_form': comment_form})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})\

def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(user=request.user)
    return render(request, 'logined/profile.html', {'user_profile': user_profile, 'user_posts': user_posts})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()


            if not user_profile.avatar:
                default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', 'default_avatar.jpg')
                with open(default_avatar_path, 'rb') as f:
                    user_profile.avatar.save('default_avatar.jpg', File(f))

            return redirect('profile')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'logined/edit_profile.html', {'form': form})

@login_required
def confirm_delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=request.user.username, password=password)

        if user is not None:
            request.user.userprofile.delete()
            user.delete()
            logout(request)
            return redirect('index')
        else:
            return render(request, 'logined/confirm_delete_account.html', {'error': 'Неправильный пароль'})

    return render(request, 'logined/confirm_delete_account.html')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'logined/create_post.html', {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.can_delete(request.user):
        post.delete()
    return redirect('index')

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.can_delete(request.user):
        comment.delete()
    return redirect('index')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.can_edit(request.user):
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = CommentForm(instance=comment)
        return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
    return redirect('index')