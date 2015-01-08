from mongoengine import *
from mongoengine.django.auth import User
import uuid


class ConfirmationCode(Document):
	user = ReferenceField(User)
	code = StringField(max_length=32)

	def confirm(self, confirmation_code):
		return self.code == confirmation_code

	@classmethod
	def create(cls, user):
		c = cls(user = user)
		c.code = uuid.uuid4().hex
		return c

class Profile(Document):
	MALE = 'Male'
	FEMALE = 'Female'

	GENDER_CHOICES = (
		MALE, FEMALE,
	)
	user = ReferenceField(User)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)
	age = IntField()
	gender = StringField(choices=GENDER_CHOICES)
	location = StringField(max_length=50)
	occupation = StringField(max_length=30)
	company = StringField(max_length=30)
	about = StringField(max_length=300)
	# picture = ImageField(size=(800, 600, True), thumbnail_size=(50, 50, True))

	def __unicode__(self):
		return str(self.id)
