from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
# from django_mysql.models import ListTextField
# from django.db.models import TextField, Model


class ques(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	likes = models.IntegerField(default=0)
	date_asked = models.DateTimeField(default=timezone.now)
	asked_by = models.CharField(max_length=50)
	liked_by = models.ManyToManyField(User , related_name = 'likes', blank = True )
	slug = models.SlugField(unique=True, blank=True, default=uuid.uuid4)

	def __str__(self):
		return self.question

	def get_like_url(self):
		return reverse("like-toggle", kwargs={"slug": self.slug})	

	def get_absolute_url(self):
		return reverse("home")		 