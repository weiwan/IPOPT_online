from django import forms
from django.contrib.auth.models import User
from models import *
from datetime import datetime
import os.path

linear_solve_choices = [("ma27", "use the Harwell routine MA27"),("ma57","use the Harwell routine MA57"),
						("ma77","use the Harwell routine HSL_MA77"),("ma86", "use the Harwell routine HSL_MA86"),
						("ma97","use the Harwell routine HSL_MA97"),("pardiso","use the Pardiso package"),
						("wsmp","use WSMP package"),("mumps","use MUMPS package")]
class SubmitForm(forms.Form):
	modelfile = forms.FileField(required=False)
	datafile = forms.FileField(required=False)
	modelcode = forms.CharField(required=False)
	datacode = forms.CharField(required=False)
	title = forms.CharField(required=True)
	comments = forms.CharField(required=False)
	sendemail = forms.BooleanField(required=False)
	email = forms.EmailField(required=True)
	linear_solve = forms.ChoiceField(required=False,choices=linear_solve_choices)
	tol = forms.FloatField(required=False,min_value=0.0)
	max_iter = forms.IntegerField(required=False,min_value=1)
	bound_frac = forms.FloatField(required=False,min_value=0.0, max_value=0.5)
	bound_push = forms.FloatField(required=False,min_value=0.0, max_value=0.5)
	option = forms.CharField(required=False)

	def save(self, f=None, commit=True):
		model = NLPModel()
		if f:
			model.f.put(f,content_type='text/plain')
			model.type = os.path.splitext(f.name)[1]
		else:
			model.f.put(self.cleaned_data['modelcode'].encode('utf-8'), content_type='text/plain')	
			model.type = ".mod"
		model.n = 1
		model.m = 2
		model.save()
		sub = Submission()
		if self.cleaned_data['option']:
			option = Option.objects.get(pk=self.cleaned_data['option'])
			sub.option = option
		else:				
			option = Option()
			if self.cleaned_data['linear_solve']:
				option.linear_solve = self.cleaned_data['linear_solve']
			if self.cleaned_data['tol']:
				option.tol = self.cleaned_data['tol']
			if self.cleaned_data['max_iter']:
				option.max_iter = self.cleaned_data['max_iter']
			if self.cleaned_data['bound_push']:
				option.bound_push = self.cleaned_data['bound_push']
			if self.cleaned_data['bound_frac']:
				option.bound_frac = self.cleaned_data['bound_frac']
			option.save()
			sub.option = option
		sub.title = self.cleaned_data['title']
		sub.model = model
		
		sub.comments = self.cleaned_data['comments']
		sub.time = datetime.now()
		sub.sendemail = self.cleaned_data['sendemail']
		sub.email = self.cleaned_data['email']
		sub.status = "Pending"
		if commit:
			sub.save()
		return sub
