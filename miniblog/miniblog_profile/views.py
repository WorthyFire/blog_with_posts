import os

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files import File
from django.shortcuts import render, redirect

from .forms import UserProfileForm, RegistrationForm
from .models import UserProfile


def index(request):
    return render(request, 'index.html')
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

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    return render(request, 'logined/profile.html', {'user_profile': user_profile})

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
