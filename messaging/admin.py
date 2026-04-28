# messaging/admin.py
from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin for the Message model.
    Field names must exactly match messaging/models.py
    """

    # 'is_read' and 'created_at' must exist in Message model.
    # Check your messaging/models.py has these exact field names.
    list_display = ['id', 'sender', 'receiver', 'content_preview', 'is_read', 'created_at']

    # Filter by read status and date.
    list_filter = ['is_read', 'created_at']

    # Search by sender/receiver username or message content.
    search_fields = ['sender__username', 'receiver__username', 'content']

    # Newest messages first.
    ordering = ['-created_at']

    # Toggle is_read directly in the list view.
    list_editable = ['is_read']

    list_per_page = 30

    def content_preview(self, obj):
        """Shows first 60 characters of message."""
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Message'