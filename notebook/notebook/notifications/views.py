from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# local import:
from .models import Notification

# Create your views here.

def show_notifications(request):
    """Load and return notification stream for a given user."""
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    template = loader.get_template('notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))
