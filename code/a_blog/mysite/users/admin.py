from django.contrib import admin

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website']
    list_display_links = ['user']
    search_fields = ['user', 'website']

admin.site.register(Profile, ProfileAdmin)

