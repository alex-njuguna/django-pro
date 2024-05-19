import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment, Reaction
from .forms import EmailPostForm, CommentForm, SearchForm, NewPostForm, PostUpdateForm

load_dotenv()

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

    # Handle reactions
    if request.method == 'POST' and 'reaction' in request.POST:
        reaction_type = request.POST.get('reaction')
        existing_reaction = Reaction.objects.filter(user=request.user, post=post).first()
        if existing_reaction:
            existing_reaction.reaction = reaction_type
            existing_reaction.save()
        else:
            Reaction.objects.create(user=request.user, post=post, reaction=reaction_type)
        return redirect(post.get_absolute_url())

    # count reactions
    love_count = post.reactions.filter(reaction=Reaction.ReactionType.LOVE).count()
    like_count = post.reactions.filter(reaction=Reaction.ReactionType.LIKE).count()
    dislike_count = post.reactions.filter(reaction=Reaction.ReactionType.DISLIKE).count()

    # list similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.order_by('-publish').distinct()

    context = {
        'post':post, 
        'comments': comments, 
        'form': form, 
        'similar_posts': similar_posts,
        'love_count': love_count,
        'like_count': like_count,
        'dislike_count': dislike_count, 
        }

    return render(request, 'blog/post_detail.xhtml', context)

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
            search_vector = SearchVector('title', 'body', config='english')
            search_query = SearchQuery(query, config='english')
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    return render(request, 'blog/search.xhtml', {'form': form, 'query': query, 'results': results})


"""posts by a specific user"""
def posts_by_user(request, user_id, tag_slug=None):
    post_list = Post.published.filter(author__id=user_id)
    author = post_list[0].author.username
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

    context = {
        'author': author,
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'blog/posts_by_user.xhtml', context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            try:
                author = request.user
                slug = slugify(form.cleaned_data['title'])
                post = form.save(commit=False)
                post.author = author
                post.slug = slug
                post.save()

                tags = form.cleaned_data['tags']
                for tag in tags:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag)
                    post.tags.add(tag_obj)

                messages.success(request, "post saved")
                return redirect('blog:post_list')
            except Exception as e:
                print(f"An error has occured: {e}")
    else:
        form = NewPostForm()

    context = {
        'form': form
    }
    return render(request, 'blog/new_post.xhtml', context)

# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     model = Post
#     fields = ['title', 'body', 'tags', 'status']
#     template_name = 'blog/update_post.xhtml'
#     success_url = reverse_lazy('blog:post_list')

@login_required
def post_update(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, instance=post)
            if form.is_valid():
                try:
                    author = request.user
                    slug = slugify(form.cleaned_data['title'])
                    post = form.save(commit=False)
                    post.author = author
                    post.slug = slug
                    post.save()

                    post.tags.clear()
                    tags = form.cleaned_data['tags']
                    for tag in tags:
                        tag_obj, _ = Tag.objects.get_or_create(name=tag)
                        post.tags.add(tag_obj)

                    messages.success(request, "post updated")
                    return redirect('blog:post_list')
                except Exception as e:
                    print(f"An error has occured: {e}")
        else:
            form = PostUpdateForm(instance=post)
    else:
        return redirect('blog:post_list')

    context = {
        'form': form,
        'title': 'update'
    }

    return render(request, 'blog//update_post.xhtml', context)

@login_required()
def delete_post(request, post_id):
    post = Post.published.get(id=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('blog:post_list')
        