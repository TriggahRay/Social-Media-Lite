from django import forms
from .models import Comment

# Defines the comment form used when posting a comment on a post.
# Like and Follow actions are handled directly in views no form needed
# because they are simple toggle actions triggered by AJAX buttons.

class CommentForm(forms.ModelForm):
    """
    Form for submitting a comment on a post.
    The post and user fields are NOT included here
    they are set in the view before saving.
    """

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write a comment...',
            'rows': 2,              
            'maxlength': 500        # Limit comments to 500 characters
        }),
        max_length=500,
        label=''                    
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        """
        Validates comment content.
        Ensures the comment is not blank 
        Prevents comments that are just spaces
        """
        content = self.cleaned_data.get('content', '').strip()

        if not content:
            raise forms.ValidationError('Comment cannot be empty.')

        if len(content) < 2:
            raise forms.ValidationError('Comment is too short.')

        return content