from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post_list.xhtml'
    paginate_by = 3

# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         # if page number is out of range
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post_list.xhtml', {'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
     status=Post.Status.PUBLISHED,
     slug=post,
     publish__year=year,
     publish__month=month,
     publish__day=day)
    return render(request, 'blog/post_detail.xhtml', {'post':post})
