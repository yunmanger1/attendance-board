from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.conf import settings

from jobapp.models import DailyJob, DailyJobTick, Job, JobGroup

import datetime

@login_required
def index(request, year=None, month=None, day=None, template_name="jobapp/mobile/index.xml"):
    list = request.user.dailyjob_set.published()
    if year and month and day:
        date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    else:
        date = datetime.datetime.today().date()
    c = RequestContext(request, {'dailyjob_list' : list, 'user': request.user, 'date' :date})
    return render_to_response(template_name, c, mimetype="application/xml")
