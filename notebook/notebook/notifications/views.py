from django.http import HttpResponse
from django.shortcuts import render, redirect
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


def delete_notification(request, noti_id):
    """Delete a notification instance."""
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show_notifications')


def count_notifications(request):
    """
    """
    user = request.user
    count_notifications = 0
    if user.is_authenticated():
        count_notifications = Notification.objects.filter(user=user, is_seen=False).count()

    return {'count_notifications': count_notifications}
