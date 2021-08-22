from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Form handle for a comment left on a post.
    """
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Comment
        # comment necessary here, don't forget ;)
        fields = ('body',)