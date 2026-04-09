from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from .models import Message
from accounts.models import User
from social.models import Notification
from posts.models import Post
from django.db.models import Q, Count

# Create your views here.
# Handles direct messaging between users.
# Covers: inbox view, conversation view, send message.

@login_required
def inbox_view(request):
    # Get all unique users that the logged-in user has had a conversation with.
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').order_by('-created_at')

    # Build a dictionary of conversations
    conversations = {}
    for msg in all_messages:
        # Determine who the other person in this conversation is.
        other_user = msg.receiver if msg.sender == request.user else msg.sender

        
        if other_user not in conversations:
            conversations[other_user] = msg

    # Count total unread messages 
    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    context = {
        'conversations': conversations,   
        'unread_count': unread_count,
    }

    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_view(request, username):
    # Get the other user 404 if they do not exist.
    other_user = get_object_or_404(User, username=username)

    # Cannot message yourself.
    if other_user == request.user:
        messages.error(request, 'You cannot message yourself.')
        return redirect('inbox')

    # Fetch the full conversation 
    conversation = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').order_by('created_at')

    # Mark all messages from the other user as read
    conversation.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # Handle sending a new message via POST form.
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            # Create and save the new message.
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

            # Notify the receiver about the new message.
            Notification.objects.create(
                user=other_user,
                sender=request.user,
                notification_type='message',
                message=f'{request.user.username} sent you a message.'
            )

            # Redirect back to the conversation page 
            # This prevents the form from resubmitting if the user refreshes.
            return redirect('conversation', username=username)
        else:
            messages.error(request, 'Message cannot be empty.')

    context = {
        'other_user': other_user,
        'conversation': conversation,
    }

    return render(request, 'messaging/conversation.html', context)


@login_required
@require_POST
def send_message_ajax_view(request, username):
    """
    AJAX version of sending a message.
    Used when JavaScript sends the message without a full page reload.
    Returns the new message data as JSON so JavaScript can
    append it to the conversation thread instantly.

    Complements conversation_view() use whichever fits your frontend.
    """
    other_user = get_object_or_404(User, username=username)

    # Cannot message yourself.
    if other_user == request.user:
        return JsonResponse({'error': 'You cannot message yourself.'}, status=400)

    content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    # Create the message in the database.
    message = Message.objects.create(
        sender=request.user,
        receiver=other_user,
        content=content
    )

    # Create a notification for the receiver.
    Notification.objects.create(
        user=other_user,
        sender=request.user,
        notification_type='message',
        message=f'{request.user.username} sent you a message.'
    )

    # Return the new message as JSON for the JavaScript to render.
    return JsonResponse({
        'success': True,
        'message': {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'created_at': message.created_at.strftime('%I:%M %p'),
            'is_mine': True,   
        }
    })

# Part of the admin search responsibility 
@login_required
def search_view(request):
    """
    AJAX powered search for users and posts.
    Accepts a query string from the URL parameter 'q'.
    Example URL: /search/?q=daniel

    Returns JSON results if the request is AJAX,
    or renders a full search results page for regular requests
    """

    q = request.GET.get('q', '').strip()

    users = []
    posts = []

    if q:
        # Search users by username or bio.
        # icontains makes the search case-insensitive.
        users = User.objects.filter(
            Q(username__icontains=q) |
            Q(bio__icontains=q)
        ).exclude(
            id=request.user.id  # Exclude the logged-in user from results
        )[:10]  # Limit to 10 results for performance

        # Search posts by content or tag name.
        posts = Post.objects.filter(
            Q(content__icontains=q) |
            Q(tags__name__icontains=q),
            visibility='public'   # Only show public posts in search results
        ).select_related('user').annotate(
            likes_count=Count('likes', distinct=True)
        ).distinct()[:10]  

    # If called via AJAX return JSON for dynamic rendering.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'users': [
                {
                    'username': u.username,
                    'bio': u.bio or '',
                    'profile_pic': u.profile_pic.url if u.profile_pic else '',
                }
                for u in users
            ],
            'posts': [
                {
                    'id': p.id,
                    'content': p.content[:100],
                    'username': p.user.username,
                    'likes_count': p.likes_count,
                }
                for p in posts
            ]
        })

    # Regular GET request render the full search results page.
    context = {
        'query': q,
        'users': users,
        'posts': posts,
    }

    return render(request, 'search/results.html', context)
