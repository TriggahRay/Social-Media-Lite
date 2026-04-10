from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration page shows the sign-up form.
    # URL: /register/
    # View: register_view in accounts/views.py
    # Name: 'register'  used in templates as {% url 'register' %}
    path('register/', views.register_view, name='register'),

    # Login page shows the sign-in form.
    # URL: /login/
    path('login/', views.login_view, name='login'),

    # Logout — destroys the session and redirects to login.
    # URL: /logout/
    # Should only be accessed via POST to prevent CSRF attacks.
    path('logout/', views.logout_view, name='logout'),

    # User profile page shows a user's posts and info.
    # URL: /profile/daniel/ (where daniel is the username)
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Edit profile page lets the logged-in user update their info.
    # URL: /profile/edit/
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]