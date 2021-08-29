from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max

# Create your models here.
class Message(models.Model):
    """
    Layout of a direct message as sent by another user and recieved by logged in user.

        Attributes:
                user: User id.
                sender: User id for message creator.
                recipient: User id for reciever of message sent. Destination.
                body: body of text content in message. Limited to 100 chars. Can be empty.
                date: timestamp message was created at.
                is_read: Boolean flag to indicate if message has been opened by recipient.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def send_message(from_user, to_user, body):
        """
        Operation for sending message class.

        Note: 2 message objects are created - one for the sender and one for the recipient.
        """
        sender_message = Message(user=from_user,
                                sender=from_user,
                                recipient=to_user,
                                body=body,
                                is_read=True
                                )
        sender_message.save()

        recipient_message = Message(user=to_user,
                                    sender=from_user,
                                    recipient=from_user,
                                    body=body
                                    )
        recipient_message.save()

        return sender_message

    def get_messages(user):
        """
        Return all messages for a given user.
        """
        # retrieve all messages for logged in user, ordering by time sent.
        messages = Message.objects.filter(user=user).values('recipient').annotate(Last=Max('date')).order_by('-last')

        # load all users who have sent messages.
        users = []
        for message in messages:
            # unread is set to false as we are looking for unseen messages:
            users.append({
                        'user': User.objects.get(pk=message['recipient']),
                        'last': message['last'],
                        'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
                        })
            
        return users
