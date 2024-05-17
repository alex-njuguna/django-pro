from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.xhtml'), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog:post_list'), name='logout'),
    path('register/', views.register_user, name='register'),
]
