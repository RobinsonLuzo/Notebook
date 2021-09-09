from django.urls import path

# local import:
from .views import show_notifications, delete_notification

urlpatterns = [
    path('', show_notifications, name='show_notifications'),
    path('<noti_id>/delete', delete_notification, name='delete_notification'),
]