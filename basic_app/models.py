from django.db import models
from django.contrib.auth.models import User


def nothin():
	pass

def info(mod):
	print(f'Dirs of {mod} are \n')
	for dir_ in dir(mod):
		print(dir_)

# Create your models here.


class UserProfile(models.Model):

	user = models.OneToOneField(User, on_delete=nothin)

	prof_url = models.URLField(blank=1)
	prof_img = models.ImageField(upload_to='user_pics', blank=1)

	# info(user)

	def __str__(self):
		return self.user.username
