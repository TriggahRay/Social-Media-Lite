from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Post, Tag
from .forms import PostForm
from social.models import Follow, Like


# Handles all post related views.
# Covers: news feed, create post, post detail, edit post, delete post.
# Create your views here.

def get(self, request, *args, **kwargs): # will run whenevr the user tries to ciew this page
        posts = Post.objects.all().order_by('-created_on') # displays posts from the most recent to the last (newest to oldest)

        context = {
            'post_list' : posts,
        }
        
        return render(request, 'social/post_list.html', context)

def feed_view(request):
    """
    Displays the main news feed showing posts from followed users.
    If the user is not logged in shows all public posts instead.
    """
    if request.user.is_authenticated:
        # Get all user IDs that the logged-in user follows.
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

        # Fetch posts from followed users the user's own posts.
        posts = Post.objects.filter(
            user_id__in=following_ids
        ) | Post.objects.filter(
            user=request.user
        )
    else:
        posts = Post.objects.filter(visibility='public')

    posts = posts.select_related('user').annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

    context = {
        'page_obj': page_obj,        
        'liked_post_ids': liked_post_ids,  
    }

    return render(request, 'posts/feed.html', context)


@login_required
def create_post_view(request):
    """
    Allows a logged-in user to create a new post.
    POST validates and saves the new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # Assign the currently logged in user as the post author.
            post.user = request.user
            post.save()
            form.save_m2m()

            messages.success(request, 'Post created successfully.')
            return redirect('feed')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


def post_detail_view(request, post_id):
    """
    Displays a single post with all its comments.
    """
    # Fetch the post or return 404 if it does not exist.
    post = get_object_or_404(
        Post.objects.select_related('user').prefetch_related(
            'comments__user',  # Fetch all comments and each comment's 
            'likes'            # Fetch all likes 
        ),
        id=post_id
    )

    # Check if the current user has liked this post.
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()

    context = {
        'post': post,
        'is_liked': is_liked,
        'likes_count': post.likes.count(),
        'comments': post.comments.all(),
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def edit_post_view(request, post_id):
    """
    Allows a user to edit their own post.
    Uses get_object_or_404 with both id and user to ensure
    a user cannot edit someone else's post by guessing the post ID.

    GET  shows the pre-filled edit form.
    POST saves the updated post content.
    """
    # The user=request.user check ensures only the owner can edit.
    # If another user tries to access this URL, they get a 404.
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        # instance=post tells Django to UPDATE this post
        # not create a brand new one.
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill the form with the current post content.
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_view(request, post_id):
    """
    Allows a user to delete their own post.
    Only accepts POST requests to prevent accidental deletion
    from someone simply visiting the URL (CSRF protection).

    After deletion, redirects to the feed with a success message.
    """
    # Only the post owner can delete, 404 if trying to delete someone else's post.
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        # delete() removes the record from the database permanently.
        # Because of CASCADE, all likes, comments and notifications
        # linked to this post are automatically deleted too.
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('feed')

    # If someone visits the delete URL with a GET request
    # show a confirmation page before deleting.
    return render(request, 'posts/delete_confirm.html', {'post': post})