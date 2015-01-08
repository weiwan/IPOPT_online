from django import forms
from models import *
from datetime import datetime

class DiscussForm(forms.Form):
	title = forms.CharField(required=True)
	text = forms.CharField(required=True)
	code = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	# def clean_tags(self):

	def save(self, user, commit=True):
		instance = Discussion()
		instance.title = self.cleaned_data['title']
		instance.text = self.cleaned_data['text']
		instance.code = self.cleaned_data['code']
		instance.user = user
		instance.time = datetime.now()
		instance.like = 0
		instance.dislike = 0
		mytags = self.cleaned_data['tags'].split(',')
		for t in mytags:
			if t != '':
				tag_instance = Tag()
				# created = Tag.objects.filter(text=tag).count()
				# if created > 0:
				# 	tag_instance.text = tag
				# 	tag_instance.count = 1
				# else:
				# 	tag_instance.count = tag_instance.count + 1
				tag_instance.text = t
				# tag_instance.count = 1
				instance.tags.append(tag_instance)
		if commit:
			instance.save()
		return instance
