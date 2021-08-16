import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
def user_directory_path(instance, filename):
    """
    Given file will be uploaded to MEDIA_ROOT, form of: user(id)/filename.

    Note: user in this instance can be a user id in numeric or character.
    """
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    """
    Hashtag implementation.
    
    Slug use ref: https://stackoverflow.com/questions/427102/what-is-a-slug-in-django
    """
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        # For when people click on the tag, create a url with given slug
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Check if hashtag has a slug, if not convert title to one and save."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    """
    An instance of a post made by the user/ content posted.

        Attributes:
                id: A unique id - uses uuid method for a non sequential unique id.
                picture: The given image.
                caption: Text associated with picture.
                tags: Social media tags associated with post.
                user = User id.
                likes = no. of likes for post.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])


class Follow(models.Model):
    """
    An .

        Attributes:
                follower: A unique follower going by follower user id.
                following: Collective of followers.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class Stream(models.Model):
    """
    A class to handle streaming of content to followers.

        Attributes:
                following: Collective of follower ids.
                user: User id.
                post: Post details to display/stream.
                date: date post created.
    """
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        """Add post to stream to followers."""
        post = instance
        # user in this case is post owner user.
        user = post.user
        # Open followers db and filter for only users who are following the given user id.
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            # For each follower, create a stream.
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


class Likes(models.Model):
    """
    A class to handle likes for a given post by a number of users.

        Attributes:
                user: User id.
                post: Post details to display.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')



# Notify recievers by sending a flag: https://docs.djangoproject.com/en/3.2/topics/signals/
# Happens every time a user makes a post:
post_save.connect(Stream.add_post, sender=Post)
