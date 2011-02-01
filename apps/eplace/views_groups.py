from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.core.urlresolvers import reverse

from eplace.utils import is_teacher, is_dean, is_superviser, get_group_lessons
from eplace.models import Subject, Group, LessonDay, Tick, Lesson, Student,\
    Superviser
from eplace.forms import TickForm, LessonDayForm, GenerateLessonDayForm
from eplace.utils import json_response, getval, get_page

import datetime
import logging

log = logging.getLogger('eplace')

############## switches ###########################
def req(f):
    def nf(request, *a, **kw):
        if (is_superviser(request.user)):
            return f(request, *a, **kw)
        if request.is_ajax():
            return json_response("ERROR")
        return HttpResponseRedirect(reverse('eplace_index'))
    return nf
############## switches ###########################

def index(request, template_name="eplace/groups/index.html"):
    superviser = request.user.superviser
    c = RequestContext(request, {'superviser' : superviser, 'curpage': 'groups'})
    return render_to_response(template_name, c)

@req
def group(request, gid, template_name="eplace/groups/group.html"):
    try:
        superviser = request.user.superviser
        group = superviser.groups.get(pk=int(gid))
        lessons = get_group_lessons(group)
    except Superviser.DoesNotExist:
        raise Http404
    except Group.DoesNotExist:
        raise Http404

    c = RequestContext(request, {'superviser': superviser, 'group': group, 'lessons': lessons})
#    return render_to_response(template_name, c)

#    if request.method == "POST":
#        lf = LessonDayForm(request.POST)
#        if lf.is_valid():
#            try:
#                o = lf.save(lesson)
#                return json_response("OK", render_to_string(template_name, c))
#            except:
#                return json_response("ERROR")

    return json_response("OK", render_to_string(template_name, c))
