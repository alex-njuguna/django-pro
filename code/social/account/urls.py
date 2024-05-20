from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_changeform.xhtml'), name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.xhtml'), name='password_change_done'),
    
    path('', views.dashboard, name='dashboard'),
]

