from django import forms
from .models import Post

class NewPostForm(forms.ModelForm):
    """
    Takes a picture
    """
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption', 'tags')
