from django.contrib.auth.forms import (
	AuthenticationForm, UserCreationForm )
from django import forms
from mongoengine.django.mongo_auth.models import MongoUser
from django.utils.translation import ugettext, ugettext_lazy as _

class UserCreationReCaptchaForm(forms.Form):
	error_messages = {
	'password_mismatch': ("The two password fields didn't match."),
	'username_already_exists': ("The username you chose already taken, please find another."),
	'email_already_exists': ("The email is already registered, maybe you need to reset password.")
	}
	username = forms.CharField(required=True)
	email = forms.EmailField(required= True)
	password1 = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput)
	password2 = forms.CharField(label=_("Password confirmation"),
		widget=forms.PasswordInput,
		help_text=_("Enter the same password as above, for verification."))

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("The two password fields didn't match.")
		return password2

	def clean_email(self):
		email = self.cleaned_data["email"]
		email_exists = MongoUser.objects.filter(email=email).count()
		if email_exists > 0:
			raise forms.ValidationError("The email is already registered, maybe you need to reset password.")
		else:
			return email

	def clean_username(self):
		username = self.cleaned_data["username"]
		username_exists = MongoUser.objects.filter(username=username).count()
		if username_exists > 0:
			raise forms.ValidationError("The username you chose already taken, please find another.")
		else:
			return username

	def save(self, commit=True):
		user = MongoUser.objects.create_user(username=self.cleaned_data["username"],
			email=self.cleaned_data["email"])
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class ChangePasswordForm(forms.Form):
	user = MongoUser()
	old_password = forms.CharField(max_length = 200,
								label='Old Password',
								widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Enter old Password'}))
	new_password = forms.CharField(max_length = 200,
								label='New Password',
								widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Enter new Password'}))
	new_password_confirm = forms.CharField(max_length = 200,
								label='Confirm New Password',
								widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Confirm new Password'}))

	def __init__(self, user=None, data=None):
		self.user = user
		super(ChangePasswordForm, self).__init__(data=data)

	def clean(self):
		cleaned_data = super(ChangePasswordForm,self).clean()
		user = MongoUser.objects.get(id = self.user.id)
		if  not user.check_password(cleaned_data.get('old_password')):
			raise forms.ValidationError("Old Password is incorrect.")
		password1 = cleaned_data.get('new_password')
		password2 = cleaned_data.get('new_password_confirm')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level form-control', 'placeholder':'Enter email Address and press enter.'}))
	def clean_email(self):
		username = self.cleaned_data.get('email')
		if not MongoUser.objects.filter(email__exact=username):
			raise forms.ValidationError("No such email in our database")
		return username

class ResetForgotPasswordForm(forms.Form):
	password1 = forms.CharField(max_length = 200,
								label='Password',
								widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Enter new password'}))
	password2 = forms.CharField(max_length = 200,
								label='Confirm Password',
								widget=forms.PasswordInput(attrs={'class':'input-block-level form-control', 'placeholder':'Confirm Password'}))
	def clean(self):
		cleaned_data = super(ResetForgotPasswordForm,self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match.")
		return cleaned_data
