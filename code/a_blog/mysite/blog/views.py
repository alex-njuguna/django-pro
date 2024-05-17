import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

load_dotenv()

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     template_name = 'blog/post_list.xhtml'
#     paginate_by = 3
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.xhtml', {'posts': posts, 'tag':tag})

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

    # list similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.order_by('-publish').distinct()

    return render(request, 'blog/post_detail.xhtml', {'post':post, 'comments': comments, 'form': form, 'similar_posts': similar_posts })

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

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/search.xhtml', {'form': form, 'query': query, 'results': results})