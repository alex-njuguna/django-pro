from django import forms
from taggit.forms import TagField

from .models import Post, Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    # email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ''  
        self.fields['email'].label = ''  
        self.fields['body'].label = ''  

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control my-2', 'placeholder': 'Email'}),
            'body': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Comment'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='')

class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['body'].label = ''
        self.fields['tags'].label = ''
        self.fields['status'].label = ''

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Body'}),
            'tags': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Tags'}),
            'status': forms.Select(attrs={'class': 'form-select my-2'}),
        }

