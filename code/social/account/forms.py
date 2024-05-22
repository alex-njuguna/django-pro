from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs= {
                'class': 'form-control, my-3',
                'placeholder': 'e.g. peter_k'
            }),
            'first_name': forms.TextInput(attrs= {
                'class': 'form-control, my-3',
                'placeholder': 'peter'
            }),
            'email': forms.TextInput(attrs= {
                'class': 'form-control, my-3',
                'placeholder': 'peter.k@example.com'
            }),
            'password1': forms.PasswordInput(attrs= {
                'class': 'form-control, my-3'
            }),
            'password2': forms.PasswordInput(attrs= {
                'class': 'form-control, my-3'
            }),
        }
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
