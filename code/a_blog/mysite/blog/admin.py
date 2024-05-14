from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    list_display_links = ['title', 'author']
    list_filter = ['status', 'created', 'publish']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierachy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)
