from django import forms
from .models import Message

# Defines the form for composing and sending a direct message.

class MessageForm(forms.ModelForm):
    """
    Form for composing a direct message to another user.
    The sender and receiver fields are NOT included here
    they are set in the view 
    """

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type a message...',
            'rows': 2,
            'maxlength': 1000
        }),
        max_length=1000,
        label=''            
    )

    class Meta:
        model = Message
        fields = ['content']

    def clean_content(self):
        """
        Validates message content.
        Prevents sending blank 
        """
        content = self.cleaned_data.get('content', '').strip()

        if not content:
            raise forms.ValidationError('Message cannot be empty.')

        return content