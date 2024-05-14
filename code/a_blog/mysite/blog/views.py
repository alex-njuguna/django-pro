from django.shortcuts import render
from django.http import Http404

from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post_list.xhtml', {'posts':posts})

def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404('No post found.')
    return render(request, 'blog/post_detail.xhtml', {'post':post})