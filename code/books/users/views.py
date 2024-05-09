from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate

# from .forms import CustomUserCreationForm


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # data validation
#             email = form.cleaned_data.get('email')
#             username = email.split('@')[0]
#             password = form.cleaned_data.get('password1')

#             # creating new user
#             user = form.save(commit=False)
#             user.username = username
#             user.save()

#             # authentication and logging in
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form, 'title': 'register'})
        
