from django.shortcuts import render
from .models import Notification
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

@login_required
def list(request):
    notifications = Notification.objects(user=request.user).order_by('-time')
    context = {}
    context['notifications'] = notifications
    if Notification.objects.filter(user=request.user, read=False).count() > 0:
        context['unread'] = True
    else:
        context['unread'] = False
    return render(request, 'notification.html', context)

@login_required
def get_notification_url(request, notification_id):
    try:
        notification = Notification.objects.get(user=request.user,id=notification_id)
    except:
        raise Http404
    notification.read = True
    notification.save()
    return redirect(notification.url)

@login_required
def markallread(request):
    notifications = Notification.objects(user=request.user).order_by('-time')
    print "hello"
    for notification in notifications:
        notification.read = True
        notification.save()
    context = {}
    context['notifications'] = notifications
    return render(request, 'notification.html', context)
