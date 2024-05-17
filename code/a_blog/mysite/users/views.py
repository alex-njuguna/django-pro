from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import RegisterUserForm


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
        'title': 'register',
    }

    return render(request, 'users/register.xhtml', context)



