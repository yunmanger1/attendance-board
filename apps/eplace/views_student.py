from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse

from eplace.models import is_teacher, is_dean, is_superviser
from eplace.models import Subject, Group, LessonDay, Tick, Student
from eplace.forms import SettingsForm, get_default_settings

from eplace.utils import json_response

import datetime

############## switches ###########################
def req(f):
    def nf(request, *a, **kw):
        if (is_teacher(request.user)):
            return f(request, *a, **kw)
        if request.is_ajax():
            return json_response("ERROR")
        return HttpResponseRedirect(reverse('eplace_index'))
    return nf
############## switches ###########################

@req
def get(request, template_name="eplace/student/index.html", limit=50):
    list = Student.objects.all()    
    page = int(request.GET.get('page',request.POST.get('page',1)))
    if request.method == "POST":
        q = request.POST.get('q',None)
        print q
        if q is not None:
            list = Student.objects.filter(name__icontains=q) | Student.objects.filter(group__title__icontains=q)
        list = list[(page-1)*limit:page*limit]
        c = RequestContext(request, {'object_list' : list})
        return json_response("OK", render_to_string("eplace/student/student-list.html", c))
    list = list[(page-1)*limit:page*limit]
    c = RequestContext(request, {'object_list' : list,'curpage':'student'})
    return render_to_response(template_name, c)
#    return json_response("ERROR")

@req
def student(request, id, template_name="eplace/student/student.html"):
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Http404
    
    
    c = RequestContext(request, {'student': student, 'curpage': 'student'})
    return render_to_response(template_name, c)