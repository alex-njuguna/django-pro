from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit', views.edit, name='edit'),

    # change password
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_changeform.xhtml'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.xhtml'), name='password_change_done'),

    # reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.xhtml'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.xhtml'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.xhtml'), name='password_reset_confirm'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.xhtml'), name='password_reset_complete'),

    # dashboard
    path('', views.dashboard, name='dashboard'),
]

