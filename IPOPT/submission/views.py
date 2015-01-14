from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from submission.models import NLPModel, Submission, Result
import os
from forms import SubmitForm
import urllib2
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.core.mail import send_mail
import json
from IPOPT.settings import pool
import redis
from random import randint


def home(request):
	if request.user.is_authenticated():
		return redirect('submission')
	else:
		context = {}
		return render(request, 'home.html', context)

# @login_required
# def submit_request(request):
# 	context = {}
# 	if request.method == 'GET':
# 		return render(request, 'submit.html',context)

# 	form = SubmitForm(request.POST)
# 	if form.is_valid():
# 		if request.FILES.has_key('modelfile'):
# 			submission = form.save(request.FILES['modelfile'])
# 		else:
# 			submission = form.save()
# 		submission.user = request.user
# 		submission.save()
# 		url = "http://"+settings.IPOPT_HOST+":"+str(settings.IPOPT_PORT)+"/WebApp/q2?id="+str(submission.id)
# 		urllib2.urlopen(url)
# 		return redirect('result')
# 		# return render(request, 'submit.html',context)

@login_required
def newsubmit(request):
	context = {}
	if request.method == 'GET':
		context['form'] = SubmitForm()
		return render(request, 'newsubmit.html', context)
	else:
		form = SubmitForm(request.POST)
		print form
		if form.is_valid():
			if request.FILES.has_key('modelfile'):
				submission = form.save(request.FILES['modelfile'])
			else:
				submission = form.save()
			submission.user = request.user
			submission.save()
			# url = "http://"+settings.IPOPT_HOST+":"+str(settings.IPOPT_PORT)+"/WebApp/q2?id="+str(submission.id)
			# urllib2.urlopen(url)
			r = redis.Redis(connection_pool = pool)
			r.rpush("IPOPT", str(submission.id))

			return redirect('result')
		else:
			raise Http404

@login_required
def result(request):
	if request.method=="GET":
		context = {}
		submissions = Submission.objects(user=request.user)
		context['submissions'] = submissions.order_by('-time')
		return render(request, 'result.html', context)
	else:
		raise Http404

@login_required
def getresultfile(request, resultID=0):
	try:
		result = Result.objects.get(pk=resultID)
	except:
		raise Http404
	context = {}
	context['result'] = result
	return render(request, 'result_detail.html', context)

@login_required
def getsubmissionfile(request, submissionID=0):
	try:
		submission = Submission.objects.get(pk=submissionID)
	except:
		raise Http404
	context = {}
	a = submission.model.f.readline()
	s = ""
	while a:
		try:
			a = a.decode()
		except:
			break
		s = s + a
		a = submission.model.f.readline()
	context['submission'] = s
	context['title'] = submission.title
	context['option'] = str(submission.option.id)
	context['editable'] = (submission.model.type == ".mod")
	return render(request, 'submission_detail.html', context)

@login_required
@require_POST
def sendresult(request, resultID=0):
	response_data = {}
	try:
		result = Result.objects.get(pk=resultID)
		request.POST['email']
		username = request.user.username
		title = username + " send you an IPOPT result"
		content = result.std
		send_mail(title, content, 'ipoptcmu@gmail.com', [request.POST['email']], fail_silently=False)
		response_data['status'] = 'Success'
		response_data['message'] = 'Result sent!'
	except:
		response_data['status'] = 'Failed'
		response_data['message'] = 'Something went wrong!'
	finally:
		return HttpResponse(json.dumps(response_data), content_type="application/json")
