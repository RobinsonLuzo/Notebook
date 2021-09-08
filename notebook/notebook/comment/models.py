from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete

# relative imports:
from notifications.models import Notification
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

    def user_comment_post(sender, instance, *args, **kwargs):
        """Generates a notification when user comments on a post."""
        comment = instance
        post = comment.post
        text_preview = comment.body[:90] #take only first 90 chars as a preview.
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        """Deletes a notification when user removes their comment."""
        comment = instance
        post = comment.post
        sender = comment.user

        notify = Notification.objects.filter(post=post, user=post.user, sender=sender, notification_type=2)
        notify.delete()


# Comment-based notifications:
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)
