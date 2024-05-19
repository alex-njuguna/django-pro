from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from.models import Profile

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-2', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control my-2 ', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control my-2 ', 'placeholder': 'Confirm Password'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-3'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'website', 'bio']
        # widgets = {
        #     'profile_pic': forms.FileInput(attrs={'class': 'form-control my-2'}),
        #     'website': forms.TextInput(attrs={'class': 'form-control my-2'}),
        #     'bio': forms.TextArea(attrs={'class': 'form-control my-2'}),
        # }
