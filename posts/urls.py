from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    # News feed the homepage for logged in users.
    # URL: /feed/
    # Shows posts from followed users own posts.
    path('feed/', views.feed_view, name='feed'),

    # Alternative feed URL same view,different URL.
    path('feed/', views.feed_view, name='feed_alt'),

    # Create a new post.
    # URL: /post/create/
    # Only accessible to logged-in users (@login_required in view).
    path('post/create/', views.create_post_view, name='create_post'),

    # View a single post and its comments.
    # URL: /post/1/ (where 1 is the post ID)
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),

    # Edit an existing post.
    # URL: /post/1/edit/
    # Only the post owner can access this (enforced in the view).
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),

    # Delete a post.
    # URL: /post/1/delete/
    # Shows a confirmation page on GET deletes on POST.
    # Only the post owner can access this 
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
]