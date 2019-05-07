from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	# add additional fields in here
	photo = models.ImageField(upload_to='images/', blank=True, default=None)

	def __str__(self):
		return '{} - {}'.format(self.username, self.email)
