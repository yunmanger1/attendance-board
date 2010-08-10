from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.conf import settings

from jobapp.models import DailyJob, DailyJobTick, Job, JobGroup
from jobapp.forms import DailyJobForm, DailyJobTickForm

import datetime

@login_required
def dailyjob_list(request, template_name="jobapp/dailyjob_list.html"):
    user = request.user
    list = DailyJob.objects.published().filter(user=user)
    c = RequestContext(request, {'object_list' : list, 'curpage': 'daily'})
    return render_to_response(template_name, c)


@login_required
def dailyjob_add(request, template_name="jobapp/dailyjob_form.html"):
    if request.method == "POST":
        form = DailyJobForm(request.POST)
        if form.is_valid():
            s = form.save(user=request.user)
            return HttpResponseRedirect(reverse('dailyjob_list'))
    else:
        form = DailyJobForm()
    c = RequestContext(request, {'form' : form, 'curpage': 'daily'})
    return render_to_response(template_name, c)

@login_required
def dailyjob_delete(request, id):
    try:
        object = DailyJob.objects.published().get(pk=id, user=request.user)
    except DailyJob.DoesNotExist:
        raise Http404
    object.is_deleted = True
    object.save()
    return HttpResponseRedirect(reverse('dailyjob_list'))

@login_required
def dailyjob_toggle(request, id):
    try:
        object = DailyJob.objects.published().get(pk=id, user=request.user)
    except DailyJob.DoesNotExist:
        raise Http404
    object.is_on = not object.is_on
    object.save()
    return HttpResponseRedirect(reverse('dailyjob_list'))

def dailyjob_done(request, id=None, date=None, tid=None, n=None, template_name="jobapp/dailyjob_tickform.html"):
    try:
        object = DailyJob.objects.published().get(pk=id, user=request.user)        
    except DailyJob.DoesNotExist:
        raise Http404
    if date == "today":
        if n is None:
            n = object.n
        tick, c = DailyJobTick.objects.get_or_create(job = object, date=datetime.datetime.today())
        tick.done = n
        tick.save() 
        #object.dailyjobtick_set.create(done=object.n, date=datetime.datetime.today())
        return HttpResponseRedirect(reverse('dailyjob_list'))
    else:
        try:
            tick = DailyJobTick.objects.get(job = object, pk=tid)
        except DailyJobTick.DoesNotExist:
            tick = DailyJobTick(job = object, done=object.n, date=datetime.datetime.today())
        if request.method == "POST":
            form = DailyJobTickForm(request.POST, instance=tick)
            if form.is_valid():
                s = form.save(job=object)
                return HttpResponseRedirect(reverse('dailyjob_list'))
        else:
            form = DailyJobTickForm(instance=tick)
        c = RequestContext(request, {'form' : form, 'curpage': 'daily'})
        return render_to_response(template_name, c)
    
def dailyjob_tickarch(request, id=None, template_name="jobapp/dailyjob_ticklist.html", **kw):
    try:
        object = DailyJob.objects.published().get(pk=id, user=request.user)        
    except DailyJob.DoesNotExist:
        raise Http404
    page_size = getattr(settings,'TICK_PAGESIZE', 60)
    page = request.GET.get('page',1)
    return list_detail.object_list(
        request,
        queryset=object.dailyjobtick_set.all().order_by('-date'),
        paginate_by=page_size,
        page=page,
        extra_context={'object':object},
        **kw
    )
