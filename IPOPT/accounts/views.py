from django.shortcuts import render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login
from .forms import UserCreationReCaptchaForm, ChangePasswordForm, ForgotPasswordForm, ResetForgotPasswordForm
from django.http import Http404, HttpResponse
from django.core.mail import send_mail
from .models import ConfirmationCode, Profile
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from mongoengine.django.auth import User
from mongoengine.django.mongo_auth.models import MongoUser
from mongoengine.django.storage import GridFSStorage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.tokens import default_token_generator
from mongoengine.django.shortcuts import get_document_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



def send_registration_confirmation(request, user):
	try:
		p = ConfirmationCode.objects.get(user = user)
	except:
		raise Http404
	title = "IPOPT account confirmation"

	confirmation_url = request.get_host() + "/accounts/confirm/" + str(p.code) + "/" + user.username + '/'
	context = {}
	context['username'] = user.username
	context['confirmation_url'] = confirmation_url
	html_content = render_to_string('email_register.html', context)
	text_content = "Welcome to IPOPT. Follow this link to activate your account. "+confirmation_url
	msg = EmailMultiAlternatives(title, text_content, 'ipoptcmu@gmail.com', [user.email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()


@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, template_name='register.html',
		  redirect_field_name=REDIRECT_FIELD_NAME,
		  usercreate_form=UserCreationReCaptchaForm,
		  current_app=None, extra_context=None):
	"""
	Displays the register form and handles the register action.
	"""
	redirect_to = request.POST.get(redirect_field_name,
								   request.GET.get(redirect_field_name, ''))

	if request.method == "POST":
		form = usercreate_form(data=request.POST)
		if form.is_valid():
			user = form.save()
			user.is_active = False
			user.save()
			# profile = Profile(user=user)
			# profile.save()
			c = ConfirmationCode.create(user)
			c.save()
			send_registration_confirmation(request, user)

			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(settings.REGISTER_REDIRECT_URL)

			return HttpResponseRedirect(redirect_to)
	else:
		form = usercreate_form()

	current_site = get_current_site(request)

	context = {
		'form': form,
		'redirect_field_name': redirect_to,
		'site': current_site,
		'site_name': current_site.name,
	}
	print form.errors
	if extra_context is not None:
		context.update(extra_context)
	return render(request, template_name, context,
							current_app=current_app)

@csrf_protect
@never_cache
def register_confirm(request, code, username):
	try:
		user = User.objects.get(username=username)
		c = ConfirmationCode.objects.get(user=user)
	except:
		raise Http404
	if c.code == code:
		user.is_active = True
		user.save()
		profile = Profile(user=user)
		profile.save()
		redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
		return render(request, 'register_confirm.html')
	else:
		raise Http404

def register_activate(request):
	return render(request, 'register_activate.html')

@login_required
@require_GET
def view_profile(request, user_id=None):
	context = {}
	if user_id:
		user = User.objects.filter(id=user_id)[0]
		context['edit_flag'] = False
	else:
		user = request.user
		context['edit_flag'] = True
	profile = get_document_or_404(Profile, user=user)
	# profile = Profile.objects.get_or_404(user=user)
	# print "profileprofile", Profile.objects.filter(user=user)
	context['profile'] = profile
	return render(request, 'view_profile.html', context)

@login_required
def edit_profile(request):
	context = {}
	user = request.user
	profile = Profile.objects.filter(user=user)[0]
	context['profile'] = profile
	print "profileprofile", Profile.objects.filter(user=user)
	if request.method == 'GET':
		return render(request, 'edit_profile.html',context)

	# newprofile = Profile()
	profile.user = user
	profile.first_name = request.POST['first_name']
	profile.last_name = request.POST['last_name']
	profile.age = request.POST['age']
	profile.gender = request.POST['gender']
	profile.location = request.POST['location']
	profile.occupation = request.POST['occupation']
	profile.company = request.POST['company']
	profile.about = request.POST['about']
	# profile.picture.replace(request.FILES['picture'], content_type="image/jpeg")

	profile.save()
	context['profile'] = profile
	print "profileprofile", Profile.objects.filter(user=user)
	return render(request, 'view_profile.html', context)

def forgot_password(request):
	context = {}
	context['success'] = 0
	if request.method=='GET':
		context['form'] = ForgotPasswordForm()
		return render(request, 'forgot_password.html', context)
	form = ForgotPasswordForm(request.POST)
	context['form'] = form
	print form.errors
	if not form.is_valid():
		return render(request, 'forgot_password.html', context)
	email = form.cleaned_data['email']
	user = User.objects.filter(email__exact=email)[0]
	token = default_token_generator.make_token(user)
	email_body = "Click the link below to reset password: http://%s%s" % (request.get_host(),reverse('reset_forgotten_password', args=(email, token)))

	send_mail(subject="Forgot IPOPT password?",
			message= email_body,
			from_email="IPOPT@IPOPT.org",
			recipient_list=[email])
	context['success'] = 1
	context['email'] = form.cleaned_data['email']
	context['confirmationUrl'] = "http://%s%s" % (request.get_host(),reverse('reset_forgotten_password', args=(email, token)))
	return render(request, 'forgot_password.html', context)

def reset_forgotten_password(request, username, token):
	context = {}
	context['token'] = token
	context['username'] = username
	user = User.objects.filter(email=username)[0]
	# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		raise Http404
	# Otherwise token was valid, listen to the GET or POST request
	if request.method=='GET':
		context['form'] = ResetForgotPasswordForm()
		return render(request, 'reset_forgotten_password.html', context)
	#Request method is post. Update password
	form = ResetForgotPasswordForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'reset_forgotten_password.html', context)
	user.set_password(form.cleaned_data['password1'])
	user.save()
	#Password Updated
	print "Password Saved"
	return redirect('/accounts/login/')

@login_required
def change_password(request):
	context = {}
	context['success'] = 0
	if request.method=='GET':
		context['form'] = ChangePasswordForm()
		return render(request, 'change_password.html', context)
	#Request method is post. Update password
	form = ChangePasswordForm(user=request.user, data=request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'change_password.html', context)
	user = request.user
	user.set_password(form.cleaned_data['new_password'])
	user.save()
	#Password Updated
	context['success'] = 1
	return render(request,'change_password.html', context)
