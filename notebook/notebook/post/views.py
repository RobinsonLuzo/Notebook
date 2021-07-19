from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

from .forms import NewPostForm
from .models import Post, Stream, Tag
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


@login_required
def PostDetails(request, post_id):
    """
    Looks for details of post as provided by id. 
    Returns 404 if not found.
    """
    post = get_object_or_404(Post, id=post_id)

    # render post object:
    template = loader.get_template('post_detail.html')
    context = {
        'post': post,
    }

    return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    """
    Creating a new post. Presumes tags are supplied correctly deliniated with commas.
    """
    user = request.user.id
    tag_obs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            # Tag lookup: creates if not existant already.
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tag_obs.append(t)

            # post creation with pic and caption:
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tag_obs)
            p.save()
            return redirect(index)

    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)


@login_required
def tags(request, tag_slug):
    """
    Generates a page of all posts citing a given tag slug/url. 

    Results are ordered by the date they were first posted.
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    # retrieve only posts with given tag:
    posts = Post.objects.filter(tags=tag).order_by('-posted') 

    template = loader.get_template('tag.html')

    context = {
        'posts': posts,
        'tag': tag,
    }

    return HttpResponse(template.render(context, request))
