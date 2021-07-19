from django.urls import path
from .views import index, NewPost, PostDetails

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetails, name='postdetails'),
]

