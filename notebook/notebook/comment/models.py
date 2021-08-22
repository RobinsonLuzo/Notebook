from django.contrib.auth.models import User
from django.db import models

from post.models import Post

# Create your models here.

class Comment(models.Model):
    """
    An instance of a comment made by a user on a given post.

        Attributes:
                post: post_id comment made to.
                user: user id of comment maker.
                body: Comment content.
                date: datestamp of comment commit.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)