from django.urls import path

# local imports
from .views import inbox, Directs

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<username>', Directs, name='directs'),
]