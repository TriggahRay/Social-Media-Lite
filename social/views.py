from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Like, Comment, Follow, Notification
from posts.models import Post
from accounts.models import User
from django.shortcuts import render

# Handles all social interaction views using AJAX.
# Covers: like/unlike, add comment, follow/unfollow, notifications.
# All views return JSON responses so JavaScript can update the
# page without reloading this is what makes the app feel modern.

@login_required
@require_POST
def like_post_view(request, post_id):
    """
    Toggles a like on a post using AJAX.
    If the user has not liked the post  creates a Like record.
    If the user already liked the post  deletes the Like record.

    @require_POST ensures this view only accepts POST requests.
    This prevents likes being triggered by simply visiting the URL.

    Returns JSON so JavaScript can update the like count and
    heart icon on the page without a full reload.

    Expected AJAX call from JavaScript:
        fetch('/like/1/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken } })
    """
    post = get_object_or_404(Post, id=post_id)

    # get_or_create() tries to find an existing Like record.
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if created:
        # New like was just created — send a notification to the post owner.
        # Only notify if someone else liked the post (not the owner liking their own post).
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,           # Who receives the notification
                sender=request.user,      # Who triggered it
                notification_type='like',
                message=f'{request.user.username} liked your post.',
                post=post                
            )
        liked = True
    else:
        like.delete()
        liked = False

    # Return updated data as JSON.
    # JavaScript uses this to update the like count and toggle the heart icon.
    return JsonResponse({
        'liked': liked,                          
        'likes_count': post.likes.count(),       
    })


@login_required
@require_POST
def add_comment_view(request, post_id):
    """
    Adds a comment to a post using AJAX.
    Receives comment content from the request body
    creates a Comment record, and returns the comment data as JSON
    so JavaScript can append it to the comments list without a page reload.

    Returns JSON containing the new comment's data.
    """
    post = get_object_or_404(Post, id=post_id)

    # Get comment content from the POST data submitted by the AJAX request.
    content = request.POST.get('content', '').strip()

    # Validate that content is not empty.
    if not content:
        # Return a 400 Bad Request response with an error message.
        return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)

    # Create and save the comment to the database.
    comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=content
    )

    # Send a notification to the post owner 
    if post.user != request.user:
        Notification.objects.create(
            user=post.user,
            sender=request.user,
            notification_type='comment',
            message=f'{request.user.username} commented on your post.',
            post=post
        )

    # Return the new comment's data as JSON.
    # JavaScript uses this to render the comment on the page immediately.
    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'username': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p'),
        },
        'comments_count': post.comments.count(),
    })


@login_required
def follow_toggle_view(request, username):
    """
    Can be called via AJAX for a seamless button toggle,
    or as a regular POST request with a redirect fallback.
    """
    # Cannot follow yourself  redirect back with an error message.
    if request.user.username == username:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('profile', username=username)

    # Get the user to follow  404 if they do not exist.
    target_user = get_object_or_404(User, username=username)

    # get_or_create() checks if the Follow relationship already exists.
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if created:
        # New follow relationship send notification to the followed user.
        Notification.objects.create(
            user=target_user,
            sender=request.user,
            notification_type='follow',
            message=f'{request.user.username} started following you.'
            # No post field follow notifications are not linked to a post.
        )
        is_following = True
    else:
        # Already following unfollow by deleting the record.
        follow.delete()
        is_following = False

    # If the request was made via AJAX (JavaScript Fetch API),
    # return a JSON response so the button can update without reload.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'followers_count': target_user.get_followers_count(),
        })

    # redirect back to the profile page.
    return redirect('profile', username=username)


@login_required
def notifications_view(request):
    """
    Displays all notifications for the logged-in user.
    Orders notifications newest first.

    After viewing marks all unread notifications as read
    so the badge count resets to zero.
    """
    notifications = Notification.objects.filter(
        user=request.user
    ).select_related('sender', 'post')

    unread_count = notifications.filter(is_read=False).count()
    notifications.filter(is_read=False).update(is_read=True)

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }

    return render(request, 'social/notifications.html', context)


@login_required
def unread_notifications_count_view(request):
    """
    Returns the count of unread notifications as JSON.
    Called periodically by JavaScript (every 30 seconds) to
    update the notification badge in the navbar without a page reload.

    JavaScript polls this endpoint using setInterval().
    """
    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return JsonResponse({'unread_count': count})