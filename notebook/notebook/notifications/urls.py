from django.urls import path

# local import:
from .views import show_notifications

urlpatterns = [
    path('', show_notifications, name='show_notifications'),
]