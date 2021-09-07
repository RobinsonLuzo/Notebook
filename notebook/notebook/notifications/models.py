from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Notification(models.Model):
    """
    Form factor for a notification - generated on action from other users.

    NOTIFICATION_TYPES: various types of valid notifications to pass.

        Attributes:
                post: post the notification is in relation to. Can be blank (i.e. Follows)
                sender: id of originator generating notification (i.e. person who liked a post)
                user: to_user for a generated notification (i.e. person whose post was liked).
                notification_type: int referencing the type of notification generated.  
                text_preview: the snippet of a comment left (if one is left).
                date: date of notification creation.           
                is_seen: boolean flag for notification acceptance by user. Similar to is_read for directs. 
    """
    # Like, subscribe, share and don't forget to ring that notification bell for more
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))

    # Note: this equates to post.models Post
    # naughty post....
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
