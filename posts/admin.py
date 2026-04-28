from django.contrib import admin
from .models import Post, Tag, PostTag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_preview', 'visibility', 'created_at', 'likes_count', 'comments_count']
    list_filter = ['visibility', 'created_at']
    search_fields = ['content', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'post_count']
    search_fields = ['name']
    ordering = ['name']

    def post_count(self, obj):
        return obj.post_tags.count()
    post_count.short_description = 'Posts using tag'


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ['post', 'tag']
    list_filter = ['tag']
    search_fields = ['post__content', 'tag__name']