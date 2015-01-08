from django.db import models
from djangotoolbox.fields import ListField

from mongoengine import *
from mongoengine.django.auth import User
# Create your models here.

class NLPModel(Document):
	f = FileField()
	n = IntField()
	m = IntField()
	type = StringField()
	meq = IntField()
	mineq = IntField()
	def __unicode__(self):
		return str(self.id)

class Result(Document):
	std = StringField()
	err = StringField()
	code = IntField()
	objective = FloatField()
	exit_tag = StringField()
	iters = IntField()

	def get_absolute_url(self):
		return '/result/%s/' % str(self.id)

	def get_id(self):
		return str(self.id)

	def __unicode__(self):
		return str(self.id)

class Option(Document):
	linear_solve = StringField(default="ma27")
	tol = FloatField(default=1e-8)
	max_iter = IntField(default=3000)
	bound_frac = FloatField(default=0.01)
	bound_push = FloatField(default=0.01)

	def __unicode__(self):
		return str(self.id)


class Submission(Document):
	title = StringField(required=True)
	user = ReferenceField(User)
	file_type = StringField(max_length=30)
	time = DateTimeField(required=True)
	model = ReferenceField(NLPModel)
	result = ReferenceField(Result)
	option = ReferenceField(Option)
	comments = StringField()
	sendemail = BooleanField()
	email = EmailField()
	status = StringField()
	start_time = DateTimeField()

	def get_absolute_url(self):
		return '/getsubmissionfile/%s/' % str(self.id)
	def get_absolute_url_result(self):
		return '/getresultfile/%s/' % str(self.result.id)
	def __unicode__(self):
		return str(self.id)
