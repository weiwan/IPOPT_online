from mongoengine import *
from mongoengine.django.auth import User


class Comment(EmbeddedDocument):
	user = ReferenceField(User)
	time = DateTimeField(required=True)
	text = StringField(required=True)

	def __unicode__(self):
		return str(self.id)


class Tag(EmbeddedDocument):
	text = StringField(required=True)
	count = IntField()

class LikedUser(EmbeddedDocument):
	user = ReferenceField(User)

class DislikedUser(EmbeddedDocument):
	user = ReferenceField(User)

class Discussion(Document):
	user = ReferenceField(User)
	time = DateTimeField(required=True)
	title = StringField(required=True)
	text = StringField(required=True)
	code = StringField()
	comments = ListField(EmbeddedDocumentField(Comment))
	tags = ListField(EmbeddedDocumentField(Tag))
	like = IntField()
	dislike = IntField()
	dislikeuser = ListField(EmbeddedDocumentField(DislikedUser))
	likeuser = ListField(EmbeddedDocumentField(LikedUser))

	def __unicode__(self):
		return	str(self.id)

	def get_absolute_url(self):
		return '/discuss/detail/%s/' % str(self.id)

	def get_id(self):
		return str(self.id)

	def get_user_id(self):
		return '/accounts/view_profile/%s/' % str(self.user.id)
