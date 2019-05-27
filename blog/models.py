from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	visits = models.BigIntegerField(default=0)
	cover = models.ImageField(upload_to='images/', blank=True, default=None)
	attachment = models.FileField(upload_to='files/', blank=True, default=None)
	opinion = models.ManyToManyField('Opinion', related_name='posts', blank=True, default=None)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return '{} - {} ({}) -> {}'.format(self.title, str(self.author), self.visits, self.published_date)

class Opinion(models.Model):
	value = models.IntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
