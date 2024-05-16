import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

load_dotenv()

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post_list.xhtml'
    paginate_by = 3


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
     status=Post.Status.PUBLISHED,
     slug=post,
     publish__year=year,
     publish__month=month,
     publish__day=day)
    comments = post.comments.filter(active=True)

    # create a comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.xhtml', {'post':post, 'comments': comments, 'form': form})

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            form_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{form_data['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}. Comments: {form_data['comments']}"
            send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), [form_data['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post_share.xhtml', {'form': form, 'post': post, 'sent': sent, 'title': 'share post'})
    