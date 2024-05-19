from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import RegisterUserForm, UserUpdateForm, ProfileUpdateForm, LoginUserForm
from blog.models import Post

def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
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

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')

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

    # get all posts by the current user that are drafts
    draft_posts = Post.objects.filter(author=request.user).filter(status=Post.Status.DRAFT)
    published_posts = Post.published.filter(author=request.user)

    context = {
        'user_form': u_form,
        'profile_form': p_form,
        'draft_posts': draft_posts,
        'published_posts': published_posts,
    }

    return render(request, 'users/profile.xhtml', context)

@login_required
def delete_user(request, user_id):
    current_user = User.objects.get(id=user_id)
    if current_user == request.user:
        current_user.delete()
        messages.info(request, "Account deleted!")
        return redirect('blog:post_list')
