from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse

from eplace.utils import is_teacher, is_dean, is_superviser
from eplace.models import Subject, Group, LessonDay, Tick, Student, Lesson
from eplace.forms import SettingsForm, get_default_settings

from eplace.utils import json_response

import datetime
from django.contrib.auth.decorators import login_required

############## switches ###########################
def req(f):
    @login_required
    def nf(request, *a, **kw):
        if (is_teacher(request.user) or is_superviser(request.user)):
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
    
    
    c = RequestContext(request, {'student': student, 'lesson_list':student.group.lesson_set.all(), 'curpage': 'student'})
    return render_to_response(template_name, c)

@req
def student_lesson(request, sid, lid, template_name="eplace/student/student.html"):
    try:
        student = Student.objects.get(pk=sid)
        lesson = Lesson.objects.get(pk=lid)
    except Student.DoesNotExist:
        return Http404
    
    c = RequestContext(request, {'student': student, 'lesson_list': [lesson], 'curpage': 'student'})
    return render_to_response(template_name, c)


@req
def lesson(request, id, template_name="eplace/student/lesson.html"):
    try:
        lesson = Lesson.objects.get(pk=id)
        lessons = lesson.lessonday_set.all()
    except Lesson.DoesNotExist:
        return Http404
    
    
    c = RequestContext(request, {'lesson': lesson, 'curpage': 'student', 'lessons' : lessons})
    return render_to_response(template_name, c)
    