from django.shortcuts import render
from submission.models import NLPModel, Result, Submission
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, Http404
import json


@login_required
@require_GET
def getData1(request):
	if request.is_ajax():
		user = request.user
		tag_dict = dict()
		submissions = Submission.objects.filter(user = user).filter(status = "Succeed")
		count = 0;
		for s in submissions:
			if s.result and s.result.exit_tag:
				count += 1
				if tag_dict.has_key(s.result.exit_tag):
					tag_dict[s.result.exit_tag] += 1
				else:
					tag_dict[s.result.exit_tag] = 1

		exit_tags = [(key, float(tag_dict[key])/count) for key in tag_dict.keys()]
		return HttpResponse(json.dumps(exit_tags), content_type="application/json")
	else:
		raise Http404

@login_required
@require_GET
def getData2(request):
	if request.is_ajax():
		response_data = {}
		user = request.user

		submissions = Submission.objects.filter(user = user).filter(status = "Succeed")
		response_data['data'] = [(d.model.n, d.model.m) for d in submissions]
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		raise Http404

@login_required
@require_GET
def getData3(request):
	if request.is_ajax():
		response_data = {}
		user = request.user
		submissions = Submission.objects.filter(user = user).filter(status = "Succeed")
		response_data['meq'] = []
		response_data['mineq'] = []
		response_data['title'] = []
		for s in list(submissions)[-20:]:
			if s.model.meq:
				response_data['title'].append(s.title)
				response_data['meq'].append(s.model.meq)
				response_data['mineq'].append(s.model.n - s.model.meq)
		print response_data
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		raise Http404

@login_required
def displayData1(request):
	return render(request, 'pie.html')

@login_required
def displayData2(request):
	return render(request, 'loglog.html')

@login_required
def displayData3(request):
	return render(request, 'stackbar.html')

@login_required
def displayAll(request):
	return render(request, 'analysis.html')