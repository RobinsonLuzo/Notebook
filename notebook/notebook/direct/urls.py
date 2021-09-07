from django.urls import path

# local imports
from .views import inbox, Directs, send_direct, search_user, new_conversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<username>', Directs, name='directs'),
    path('send/', send_direct, name='send_direct'),
    path('new/', search_user, name='usersearch'),
    path('new/<username>', new_conversation, name='newconversation'),
]