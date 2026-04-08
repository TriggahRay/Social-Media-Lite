from django import forms
from .models import Post, Tag


# Defines forms for creating and editing posts.
class PostForm(forms.ModelForm):
    """
    Handles post creation and editing.
    """

    # Main post content the text body of the post.
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "What's on your mind?",
            'rows': 4,
            'maxlength': 2000       # Limits post length to 2000 characters
        }),
        max_length=2000
    )

    # Optional image attachment.
    # ClearableFileInput shows a Clear checkbox when editing an existing post.
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'     
        })
    )

    # Visibility selector  controls who can see the post.
    # Renders as a dropdown in the template.
    visibility = forms.ChoiceField(
        choices=Post.VISIBILITY_CHOICES,
        initial='public',
        widget=forms.Select(attrs={
            'class': 'form-select'  
        })
    )

    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add tags separated by commas: python, django, webdev'
        }),
        help_text='Separate tags with commas. No # symbol needed.'
    )

    class Meta:
        model = Post
        fields = ['content', 'image', 'visibility']

    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')

        tag_names = [
            tag.strip().lower()
            for tag in tags_input.split(',')
            if tag.strip()          
        ]

        # Validate each tag name only letters, numbers, underscores allowed.
        import re
        for tag_name in tag_names:
            if not re.match(r'^[a-zA-Z0-9_]+$', tag_name):
                raise forms.ValidationError(
                    f'Tag "{tag_name}" contains invalid characters. '
                    'Only letters, numbers, and underscores are allowed.'
                )
            if len(tag_name) > 50:
                raise forms.ValidationError(
                    f'Tag "{tag_name}" is too long. Maximum 50 characters.'
                )

        return tag_names

    def save(self, commit=True):
        post = super().save(commit=commit)

        if commit:
            tag_names = self.cleaned_data.get('tags_input', [])
            post.tags.clear()

            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                
                post.tags.add(tag)

        return post