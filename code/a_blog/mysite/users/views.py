from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import RegisterUserForm, UserUpdateForm, ProfileUpdateForm, LoginUserForm


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request)
                return redirect('blog:post_list')
            else:
                messages.warning(request, "Invalid details")
        else:
            messages.warning(request, "Invalid details")
    else:
        form = LoginUserForm()

    context = {
        'form': form
    }
    
    return render(request, 'users/login.xhtml', context)


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('users:login')
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
        'title': 'register',
    }

    return render(request, 'users/register.xhtml', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated successfully")
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': u_form,
        'profile_form': p_form,
    }

    return render(request, 'users/profile.xhtml', context)

