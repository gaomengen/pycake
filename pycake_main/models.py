from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Topic(models.Model):
	"""A topic user is learning about."""
	name = models.CharField(max_length=200)
	hyphenated_topic = models.CharField(max_length=200, null=True)
	description = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, models.CASCADE)
	
	def __str__(self):
		"""Return a string representation of the model."""
		return self.name

class Subject(models.Model):
	"""Subject under Topic"""
	name = models.CharField(max_length=200)
	hyphenated_name = models.CharField(max_length=200, null=True)
	topic = models.ForeignKey(Topic, models.CASCADE)
	owner = models.ForeignKey(User, models.CASCADE)

	def __str__(self):
		"""Return a string representation of the model"""
		return self.name

class Entry(models.Model):
        """Something specific learned about a topic."""
        topic = models.ForeignKey(Topic, models.CASCADE)
        subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        hyphenated_title = models.CharField(max_length=200)
        text = RichTextUploadingField(config_name='test_config')
        date_added = models.DateTimeField(auto_now_add=True)
        owner = models.ForeignKey(User, models.CASCADE)

        class Meta:
                verbose_name_plural = 'entries'

        def __str__(self):
                """Return a string representation of the model."""
                return self.text[:50] + "..."

# Potentially add comments model here. 
