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
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        # For when people click on the tag, create a url with given slug
        return reverse('tags', arg=[self.slug])

    def __str__(self):
        self.title

    def save(self, *args, **kwargs):
        """Check if hashtag has a slug, if not convert title to one and save."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(model.Model):
    """
    An instance of a Post.

        Attributes:
                id: A unique id - uses uuid method for a non sequential unique id
                picture: The given image
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture')