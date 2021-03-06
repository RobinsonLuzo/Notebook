import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PIL import Image

# relative import:
from post.models import Post

# Create your models here.
def user_directory_path(instance, filename):
	"""
    Given file will be uploaded to MEDIA_ROOT, form of: user(id)/filename.
    Note: user in this instance can be a user id in numeric or character.
    """
	profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
	full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

	if os.path.exists(full_path):
		os.remove(full_path)

	return profile_pic_name


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

	def save(self, *args, **kwargs):
		"""Override of picture as uploaded by user. Resize given picture and resave."""
		super().save(*args, **kwargs)

		SIZE = 350, 350

		# check if a picture was actually uploaded as it can be empty.
		if self.picture:
			pic = Image.open(self.picture.path)
			# for LANCZOS example see: https://www.programcreek.com/python/example/89920/PIL.Image.LANCZOS
			pic.thumbnail(SIZE, Image.LANCZOS)
			pic.save(self.picture.path)


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)