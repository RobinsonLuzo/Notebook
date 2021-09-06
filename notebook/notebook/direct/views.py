from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
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

    # Note: keep out of if statement, otherwise returns error if messages box is empty.
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    template = loader.get_template('direct/direct.html')

    return HttpResponse(template.render(context, request))


@login_required
def Directs(request, username):
    """
    Return all messages/directs for a given username. Sent to the actively logged in user.
    """
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username

    # now filter and get all directs for that username and the actively logged in user.
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    template = loader.get_template('direct/direct.html')

    return HttpResponse(template.render(context, request))


@login_required
def SendDirect(request):
    """
    Takes input from textbox in inbox and creates a message object from it. Text only for now.
    """
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')

    else:
        HttpResponseBadRequest()


@login_required
def SearchUser(request):
    """Handles a search request for other users usernames - handled from direct page."""
    query = request.GET.get('q')
    context = {}

    if query:
        # Q is complex lookup. See: https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
        }

    template = loader.get_template('direct/search_user.html')

    return HttpResponse(template.render(context, request))
