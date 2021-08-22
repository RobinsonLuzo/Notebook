from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import resolve, reverse

from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from authy.models import Profile
from post.models import Post, Follow, Stream

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	# if profile selected then yield all posts made by user, else yield favorite/saved photos:
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
	else:
		posts = profile.favorites.all()

	# Profile info:
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	# Check follow status:
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile': profile,
		'url_name': url_name,
		'posts_count': posts_count,
		'following_count': following_count,
		'followers_count': followers_count,
		'follow_status': follow_status,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('edit-profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	"""
	Allow for a given user to create a following object showing them photos from another user.

	If currently following that users then they should unfollow.
	"""
	user = request.user
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=user, following=following)

		# if follow option flag set to 0 then unfollow:
		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			# return of first 10 posts is arbitrary - change if wanted.
			posts = Post.objects.all().filter(user=following)[:10]

			# See doc: https://stackoverflow.com/questions/34730385/django-rollback-save-with-transaction-atomic
			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=user, date=post.posted, following=following)
					stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))
