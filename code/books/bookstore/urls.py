from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # user management
    path('accounts/', include('allauth.urls')),

    # local apps
    path('', include('pages.urls')),
    path('books/', include('books.urls')),
]
