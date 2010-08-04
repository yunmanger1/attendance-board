from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.conf import settings

from jobapp.models import DailyJob, DailyJobTick, Job, JobGroup
from jobapp.forms import DailyJobForm, DailyJobTickForm

import datetime, random

@login_required
def stat_home(request, template_name="jobapp/stat/home.html"):
    c = RequestContext(request, {'curpage': 'stat'})
    return render_to_response(template_name, c)

@login_required
def stat_dailyjob(request, id, template_name="jobapp/stat/dailyjob.html"):
    job = DailyJob.objects.published().get(pk=id, user=request.user)
    ticks = job.dailyjobtick_set.all().only('date','done').order_by('date')
    t = tuple([x.date for x in ticks])
    cur = t[0]# - datetime.timedelta(days=366)
    start = cur
    dt = datetime.timedelta(days=1)
    today = datetime.datetime.today().date() 
    i = 0
    ser = []
    while cur <= today:
        try:
            k = t.index(cur)
            ser.append(int(ticks[k].done))
        except ValueError:
            ser.append(int(0))
            #ser.append(int(random.randint(1,10)))
        i+=1
        cur = cur + dt
    res = str(ser)
    c = RequestContext(request, {'curpage': 'stat', 'num': i, 'serie': res, 'object': job, 'start': start})
    return render_to_response(template_name, c)
    
