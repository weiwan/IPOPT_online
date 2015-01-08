from models import Discussion, Comment, Tag, LikedUser, DislikedUser
from mongoengine.django.auth import User
from forms import DiscussForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse,Http404
from submission.models import Result
from notification.models import Notification
import json
from mongoengine.django.shortcuts import get_document_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q


@login_required
@require_GET
def discuss(request):
	context = {}
	context['topics'] = Discussion.objects.order_by('-time')
	return render(request, 'discuss.html', context)

@login_required
def createDiscuss(request, resultID=None):
	if request.method=="GET":
		if resultID:
			result = get_document_or_404(Result, pk=resultID)
			form = DiscussForm({'title':' ', 'text':' ','code': result.std})
		else:
			form = DiscussForm()
		context = {}
		context['form'] = form
		return render(request, 'discuss_create.html', context)
	if request.method=="POST":
		form = DiscussForm(request.POST)
		if form.is_valid():
			print "inhere"
			form.save(request.user)
			return redirect('discuss')
		else:
			context = {}
			context['form'] = form
			return render(request, 'discuss_create.html', context)

@login_required
@require_GET
def myDiscuss(request):
	discussions = Discussion.objects(user=request.user).order_by('-time')
	context = {}
	context['topics'] = discussions
	return render(request, 'discuss.html', context)

@login_required
@require_GET
def findDiscuss(request, tagtext):
	t = Tag()
	t.text = tagtext
	discussions = Discussion.objects().all().order_by('-time')
	out_discussions = []
	for disc in discussions:
		if t in disc.tags:
			out_discussions.append(disc)
	context = {}
	context['topics'] = out_discussions
	return render(request, 'discuss.html', context)

@login_required
def search(request):
	context = {}
	if request.method=='GET' or not request.POST['search']:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	searchText = request.POST['search']
	# discussions = Discussion.objects.filter(((text__icontains = searchText))).order_by('-time')
		# | (code__icontains = searchText)
		# | (title__icontains = searchText)
	discussions = Discussion.objects.filter(text__icontains = searchText).order_by('-time')
	#  OR Discussion.objects.filter(code__icontains = searchText)
	context['topics'] = discussions
	print discussions
	return render(request, 'discuss.html', context)

@login_required
@require_GET
def discuss_detail(request, discussionID=0):
	context = {}
	try:
		discuss = Discussion.objects.get(pk=discussionID)
	except:
		raise Http404
	comments = discuss.comments
	context['discuss'] = discuss
	if discuss.like:
		context['like'] = discuss.like
	else:
		context['like'] = 0
	if discuss.dislike:
		context['dislike'] = discuss.dislike
	else:
		context['dislike'] = 0
	lu = LikedUser()
	lu.user = request.user
	dlu = DislikedUser()
	dlu.user = request.user
	print lu
	if dlu in discuss.dislikeuser:
		context['dislike_disable'] = True
	else:
		context['dislike_disable'] = False
	if lu in discuss.likeuser:
		context['like_disable'] = True
	else:
		context['like_disable'] = False
	context['comments'] = comments
	return render(request, 'discuss_detail.html', context)

@login_required
@require_POST
def postComment(request, discussionID):
	if request.is_ajax():
		try:
			discuss = Discussion.objects.get(pk=discussionID)
		except:
			raise Http404
		comment = Comment()
		comment.user = request.user
		comment.time = datetime.now()
		comment.text = request.POST['text']
		discuss.comments.append(comment)
		discuss.save()

		notification = Notification()
		notification.title = request.user.username + " commented on your discussion: " + discuss.title
		notification.url = discuss.get_absolute_url()
		notification.user = discuss.user
		notification.time = datetime.now()
		notification.read = False
		notification.save()

		context = {}
		context['comment'] = comment
		rendered = render_to_string('comment_row.html', context)
		return HttpResponse(json.dumps(rendered), content_type="application/json")
	else:
		raise Http404

@login_required
def dislike(request, discussionID):
	return_data = {}
	if request.is_ajax():
		discuss = Discussion.objects.get(pk=discussionID)
		if not discuss.dislike:
			discuss.dislike = 1
		else:
			discuss.dislike = discuss.dislike + 1
		dlu = DislikedUser()
		dlu.user = request.user
		return_data["dislike"] = discuss.dislike
		return_data["dislike_disable"] = True
		if dlu not in discuss.dislikeuser:
			discuss.dislikeuser.append(dlu)
		discuss.save()
		return HttpResponse(json.dumps(return_data), content_type="application/json")
	else:
		raise Http404

def like(request, discussionID):
	return_data = {}
	if request.is_ajax():
		try:
			discuss = Discussion.objects.get(pk=discussionID)
		except:
			raise Http404
		if not discuss.like:
			discuss.like = 1
		else:
			discuss.like = discuss.like + 1
		lu = LikedUser()
		lu.user = request.user
		return_data["like"] = discuss.like
		return_data["like_disable"] = True
		if lu not in discuss.likeuser:
			discuss.likeuser.append(lu)
		discuss.save()
		return HttpResponse(json.dumps(return_data), content_type="application/json")
	else:
		raise Http404
