from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

from authy.models import Profile
from comment.forms import CommentForm
from comment.models import Comment

from .forms import NewPostForm
from .models import Post, Stream, Tag, Likes
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
    user = request.user
    favorited = False

    # Comment check:
    comments = Comment.objects.filter(post=post).order_by('date')

    # if comment being given:
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()

            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

    else:
        form = CommentForm()

    # favorite flag check:
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # if post id is already saved by user:
        if profile.favorites.filter(id=post_id).exists():
            favorited = True

    # render post object:
    template = loader.get_template('post_detail.html')
    context = {
        'post': post,
        'favorited': favorited, 
        'form': form,
        'comments': comments,
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

            # strip out whitespace and reserved characters like # also:
            reserved_list = "#"
            for char in reserved_list:
                tags_form = tags_form.replace(char, "")

            tags_list = tags_form.replace(" ", "").split(',')
            #tags_list = list(tags_form.split(','))

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


@login_required
def like(request, post_id):
    """
    Handles a like being given by a user to a given post.

    If a user likes a post, the like count is incremented by one and the like added to the db. 
    If the specific user has already liked a given post then it will be unliked and the like removed from the db.

    NOTE: the number of likes a post has is a local count here - it is not stored in the db, 
    but rather counted from it and modified locally in this function with a local variable.
    """
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post).count()

    # if not likes returned to liked then create one:
    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1

    # else remove like as user is unliking that post
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


@login_required
def favorite(request, post_id):
    """
    Handles a save/favorite by a user for a specific post.

    Find and load the user profile and check if the user has saved/favorited the post already.
    If so then unsave the post from their favorites. Otherwise add it in.
    """
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    
    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))