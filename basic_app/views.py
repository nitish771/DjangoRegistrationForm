from django.shortcuts import render
from basic_app.forms import UserProfileForm, UserForm

from django.contrib.auth import (
	authenticate,
	login,
	logout
)
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
	return render(request, 'basic_app/index.html')


def register(request):
	registered = False
	user_form = None
	prof_form = None

	if request.method == 'POST':
		# print(request, 'dirs', '\n', dir(request))
		user_form = UserForm(data=request.POST)
		prof_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and prof_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = prof_form.save(commit=False)
			profile.user = user

			# check if image is uploaded
			if 'prof_img' in request.FILES:
				profile.prof_img = request.FILES['prof_img']
			profile.save()
			registered = True

		else:  # if invalid
			print(user_form.errors, prof_form.errors)

	else:
		user_form = UserForm()
		prof_form = UserProfileForm()

	return render(request, 'basic_app/registration.html', context={
		'user_form': user_form,
		'prof_form': prof_form,
		'registered': registered,
		})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("You're account has been deactivated!")
		else:
			msg = ("Looks like you got a stargazer. Watchout and change your passsword\n"
					"Last login creds {} : {}".format(username, password))
			return HttpResponse(msg) 
	else:  # not filled form
		return render(request, 'basic_app/login.html')


@login_required
def special(request):
	return HttpResponse('You\'re logged in. Great!')


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('basic_app:login'))


@login_required
def other(request):
	return HttpResponse("You're not logged in. Please Login to access url.")
