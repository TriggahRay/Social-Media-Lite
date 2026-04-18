# social/admin.py
from django.contrib import admin
from .models import Comment, Like, Follow, Notification


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']
    ordering = ['-created_at']
    list_per_page = 30

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Comment'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['-created_at']
    list_per_page = 50


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Follow model only has: follower, following, created_at
    The error said 'created_at' is not a field — which means
    your Follow model is missing created_at. Fix below.
    """
    list_display = ['id', 'follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    ordering = ['-created_at']
    list_per_page = 50


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    The error said 'sender' is not a field on Notification.
    Your Notification model must have a sender ForeignKey.
    Fix the model below if missing.
    """
    list_display = ['id', 'user', 'sender', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']
    ordering = ['-created_at']
    list_editable = ['is_read']
    list_per_page = 30