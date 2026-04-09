from django.urls import path
from . import views
from posts import views as post_views  

app_name = 'messaging'

urlpatterns = [
    # Inbox shows a list of all conversations.
    # URL: /inbox/
    path('inbox/', views.inbox_view, name='inbox'),

    # Shows the full message history between the two users.
    # Also handles sending new messages via POST form.
    path('messages/<str:username>/', views.conversation_view, name='conversation'),

    # Send a message via AJAX  returns JSON.
    # URL: /messages/daniel/send/
    # Method: POST only (@require_POST in the view).
    # Returns: JSON with the new message data.
    # JavaScript calls this when the user hits Send in the chat window.
    path('messages/<str:username>/send/', views.send_message_ajax_view, name='send_message'),

    # Search for users and posts AJAX + regular GET.
    # URL: /search/?q=daniel
    # Returns JSON if called via AJAX (for live search dropdown).
    # Returns full page if accessed normally 
    path('search/', views.search_view, name='search'),
]