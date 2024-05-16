from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    list_display_links = ['title', 'author']
    list_filter = ['status', 'created', 'publish']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierachy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'updated', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

admin.site.register(Comment, CommentAdmin)
