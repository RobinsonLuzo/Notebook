from django.urls import path

# local imports
from .views import inbox, Directs, SendDirect, SearchUser, NewConversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<username>', Directs, name='directs'),
    path('send/', SendDirect, name='send_direct'),
    path('new/', SearchUser, name='usersearch'),
    path('new/<username>', NewConversation, name='newconversation'),
]