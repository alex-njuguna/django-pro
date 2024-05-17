from django.contrib import admin

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']
    list_display_links = ['user']
    search_fields = ['user', 'email']

admin.site.register(Profile, ProfileAdmin)

