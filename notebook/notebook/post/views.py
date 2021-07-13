from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Post, Stream
# Create your views here.

# For login_required decorator see: https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-login-required-decorator

@login_required
def index(request):
    """
    Retrieve all stream objects created for the user, get their post ids
    then filter all posts for only these ids. Put the results into a page.
    """
    user = request.user
    # Loading from Stream, not an individual post
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    # in__in: https://stackoverflow.com/questions/2354284/django-queries-how-to-filter-objects-to-exclude-id-which-is-in-a-list
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,
    }

    return HttpResponse(template.render(context, request))