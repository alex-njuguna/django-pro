from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts
    path('account/', include('account.urls')),
]
