from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User


# Covers: user registration, login, and profile editing.
# Django forms handle validation, rendering and saving of form data.

class RegisterForm(UserCreationForm):
    """
    Handles new user registration.
    Extends Django's built-in UserCreationForm which already provides:
    - username field
    - password1 field (password entry)
    - password2 field (password confirmation)
    - password matching validation
    - password strength validation

    We add email, first_name, last_name, and bio on top.
    """

    # Email field required for registration.
    # EmailField automatically validates proper email format (user@example.com)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',        
            'placeholder': 'Enter your email address'
        }),
        help_text='A valid email address is required.'
    )

    # First name 
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )

    # Last name 
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )

    # Bio 
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us a little about yourself...',
            'rows': 3               # Controls the visible height of the textarea
        })
    )

    class Meta:
        """
        Meta class tells Django which model this form is based on
        and which fields to include in the form.
        """
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def clean_username(self):
        """
        Custom validation for the username field.

        Rules:
        - Must be between 3 and 30 characters long.
        - Can only contain letters, numbers, and underscores.
        - Must not already be taken by another user.
        """
        username = self.cleaned_data.get('username')

        # Check minimum length.
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')

        # Check for invalid characters using a regex pattern.
        # ^[a-zA-Z0-9_]+$ means: only letters, digits and underscores allowed.
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError(
                'Username can only contain letters, numbers, and underscores.'
            )

        # Check if the username is already taken by another user.
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')

        return username

    def clean_email(self):
        """
        Custom validation to ensure email addresses are unique.
        Two users cannot register with the same email address.
        """
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')

        return email

    def clean_password1(self):
        """
        Custom password strength validation on top of Django's defaults.
        Rules:
        - At least 8 characters long.
        - Must contain at least one uppercase letter.
        - Must contain at least one digit.
        - Must contain at least one special character.
        """
        import re
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')

        if not re.search(r'\d', password):
            raise forms.ValidationError('Password must contain at least one digit.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Password must contain at least one special character.')

        return password

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.bio = self.cleaned_data.get('bio')

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    # Username input field.
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True      
        })
    )

    # Password input field.
    # PasswordInput hides the typed characters (shows dots instead)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class ProfileEditForm(forms.ModelForm):
    """
    Allows a logged-in user to update their profile information.
    Uses ModelForm so it reads from and saves directly to the User model.
    """

    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )

    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )

    # Bio text area for the user's self-description.
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself...',
            'rows': 4
        })
    )

    # Profile picture upload field.
    # ClearableFileInput allows the user to remove their current picture.
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_pic']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use by another account.')

        return email