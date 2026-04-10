from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    # Like or unlike a post AJAX endpoint.
    # URL: /like/1/ (where 1 is the post ID)
    # Method: POST only (@require_POST in the view).
    # Returns: JSON {liked: true/false, likes_count: 5 }
    # JavaScript calls this when the user clicks the heart icon
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),

    # Add a comment to a post AJAX endpoint.
    # URL: /comment/1/ 
    # Method: POST only.
    # Returns: JSON with the new comment data.
    # JavaScript calls this when the user submits the comment form.
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment'),

    # Follow or unfollow a user.
    # URL: /follow/daniel/ 
    # Works as both AJAX (returns JSON) and regular POST (redirects).
    path('follow/<str:username>/', views.follow_toggle_view, name='follow_toggle'),

    # Notifications page shows all notifications for the logged-in user.
    # URL: /notifications/
    # Marks all notifications as read when visited.
    path('notifications/', views.notifications_view, name='notifications'),

    # URL: /notifications/count/
    # Returns: JSON { unread_count: 3 }
    path('notifications/count/', views.unread_notifications_count_view, name='notification_count'),
]