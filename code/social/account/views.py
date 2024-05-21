from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    # authenticate and login a user
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return HttpResponse('user is disabled')
    else:
        form = LoginForm()
    context = {
        'form': form,
        'title': 'login',
    }

    return render(request, 'account/login.xhtml', context)

@login_required
def user_logout(request):
    # logout a user
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # user to access dashboard
    context = {
        'title': 'dashboard'
    }
    return render(request, 'account/dashboard.xhtml', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_user = form.save(commit=False)
            new_user.save()
            # create the user profile
            Profile.objects.create(user=new_user)
            messages.success(request, f"Account for username '{username}' created successfully")
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title': 'register',
    }
    
    return render(request, 'account/register.xhtml', context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Data not correctly loaded')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'profile update'
    }

    return render(request, 'account/edit.xhtml', context)
    

    
