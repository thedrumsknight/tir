from django.conf import settings
from django.db import models


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')

class Player(models.Model):
	name = models.CharField(max_length=50)
	points = models.IntegerField(default=0)

	def __str__(self):
		return self.name