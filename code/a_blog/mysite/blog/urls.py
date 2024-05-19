from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # path('', views.PostListView.as_view(),  name='post_list'),
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('posts-by-user/<int:user_id>/', views.posts_by_user, name='user_content'),

    # posts crud
    path('new/', views.new_post, name='new_post'),
    path('<int:post_id>/update/', views.post_update, name='post_update'),
    path('<int:post_id>/delete', views.delete_post, name='delete_post')
]
