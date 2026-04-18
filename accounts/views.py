from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import User
from social.models import Follow

# Handles all user authentication and profile management views.
# Covers: registration, login, logout, profile viewing, profile editing.

# Create your views here.
def register_view(request):
    # If the user is already logged in send them to the feed.
    # No point showing the register page to authenticated users.
    if request.user.is_authenticated:
        return redirect('posts:feed')
    
    if request.method == 'POST':       
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'accounts/register.html', {'form': form})
    
    else:
        # GET request show a blank registration form.
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  
            if user is not None:
                # login() attaches the user to the current session.
                # Django sets a signed session cookie in the browser.
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')

                # If the user was redirected to login from a protected page
                # send them back there. Otherwise go to the feed.
                next_url = request.GET.get('next',)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('posts:feed')
                #return redirect(next_url)
            else:
                # Credentials did not match any user in the database.
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Logs the user out by destroying their session.
    logout() clears all session data and removes the session cookie.
    Only accessible to logged-in users (@login_required).
    Redirects to the login page after logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


def profile_view(request, username):
    # Fetch the profile owner, 404 if username doesn't exist.
    profile_user = get_object_or_404(User, username=username)

    # Fetch all posts by this user, newest first.
    posts = profile_user.posts.select_related('user').annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments')
    )

    # Used to show the Follow or Unfollow button on the template.
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile_user.get_followers_count(),
        'following_count': profile_user.get_following_count(),
        'posts_count': profile_user.get_posts_count(),
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # instance=request.user tells Django to UPDATE this user
        # rather than create a new one.
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre fill the form with the current user's data.
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form, 'hide_bottom_nav': True,})