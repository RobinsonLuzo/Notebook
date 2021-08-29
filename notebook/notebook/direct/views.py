from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# local imports
from .models import Message

@login_required
def inbox(request):
    """
    Inbox for a specific logged-in user.
    """
    user = request.user
    messages = Message.get_messages(user=user)
    # formerly active_user
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        # set read flag to true as the DM is now opened.
        directs.update(is_read=True)

        # retrieve the rest of messages from said user:
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct,
        }

    template = loader.get_template('direct/direct.html')

    return HttpResponse(template.render(context, request))
