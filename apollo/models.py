from django.conf import settings
from django.db import models
from django.utils import timezone


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')

class Player(models.Model):
	name = models.CharField(max_length=50)
	points = models.IntegerField(default=0)
	is_logged_in = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class TargetWord(models.Model):
	word = models.CharField(max_length=30)
	datetime = models.DateTimeField(default=timezone.now, db_index=True)

	def __str__(self):
		return self.word

