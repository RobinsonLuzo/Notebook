from django.urls import path

# local imports
from .views import inbox

urlpatterns = [
    path('', inbox, name='inbox'),
]