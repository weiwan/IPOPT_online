from django.db import models
from djangotoolbox.fields import ListField

from mongoengine import *
from mongoengine.django.auth import User


class Notification(Document):
	time = DateTimeField()
	user = ReferenceField(User)
	read = BooleanField()
	title = StringField()
	url = StringField()


	def __unicode__(self):
		return str(self.id)