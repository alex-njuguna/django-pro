from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Logged in')
                else:
                    return HttpResponse('user is disabled')
            else:
                return HttpResponse('invalid login details')
    else:
        form = LoginForm()
    context = {
        'form': form,
        'title': 'login',
    }

    return render(request, 'accounts/login.xhtml', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')