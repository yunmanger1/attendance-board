from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.core.urlresolvers import reverse

from eplace.utils import is_teacher, is_dean, is_superviser
from eplace.models import Subject, Group, LessonDay, Tick, Lesson, Student
from eplace.forms import TickForm, LessonDayForm, GenerateLessonDayForm
from eplace.utils import json_response, getval, get_page

import datetime
import logging
from django.contrib.auth.decorators import login_required

log = logging.getLogger('eplace')

############## switches ###########################
def req(f):
    @login_required
    def nf(request, *a, **kw):
        if (is_teacher(request.user)):
            return f(request, *a, **kw)
        if request.is_ajax():
            return json_response("ERROR")
        return HttpResponseRedirect(reverse('eplace_index'))
    return nf
############## switches ###########################

def index(request, template_name="eplace/teacher/index.html"):
    teacher = request.user.teacher
    c = RequestContext(request, {'teacher' : teacher, 'curpage': 'teachers'})
    return render_to_response(template_name, c)

@req
def subject(request, lid, template_name="eplace/teacher/subject.html"):
    try:
        teacher = request.user.teacher
        lesson = teacher.lesson_set.get(pk=int(lid))
        lessons = lesson.lessonday_set.all()
    except Subject.DoesNotExist:
        raise Http404
    except Group.DoesNotExist:
        raise Http404

    today = datetime.datetime.today().date()
    lf = LessonDayForm(initial={'date': today })
    glf = GenerateLessonDayForm(initial={'start_date': today, 'end_date': today})
    
    c = RequestContext(request, {'glf_form': glf, 'lesson_form':lf, 'lesson': lesson, 'teacher': teacher, 'lessons': lessons})
#    return render_to_response(template_name, c)

    if request.method == "POST":
        lf = LessonDayForm(request.POST)
        if lf.is_valid():
            try:
                o = lf.save(lesson)
                return json_response("OK", render_to_string(template_name, c))
            except:
                return json_response("ERROR")

    return json_response("OK", render_to_string(template_name, c))

@req
def generate(request, lid):
    try:
        teacher = request.user.teacher
        lesson = teacher.lesson_set.get(pk=int(lid))
        lessons = lesson.lessonday_set.all()
    except Lesson.DoesNotExist:
        raise Http404

    if request.method == "POST":
        glf = GenerateLessonDayForm(request.POST)
        if glf.is_valid():
            try:
                glf.save(lesson)
                return json_response("OK",get_page(request))
            except:
                import traceback
                traceback.print_exc()
                return json_response("CANT SAVE")
        else:
            log.debug(glf.errors)
            return json_response("INVALID FORM")
    return json_response("ERROR")

def save_tick(l, lesson):
    t = l.split(':')
    ld = lesson.lessonday_set.get(pk=int(t[0]))
    student = Student.objects.get(pk=int(t[1]))
    value = getval(lesson, t[2])
    if value is None:
        return None    
    try:
        tick = Tick.objects.filter(ld=ld, student=student).order_by('-pub_date')[0]
        if tick.value != value:
            raise IndexError
    except IndexError:
        tick = Tick.objects.create(ld=ld, student=student, value=value)
    return tick

@req
def tick_save(request):
    teacher = request.user.teacher
    if request.method == "POST":
        form = TickForm(teacher, request.POST)
        if form.is_valid():
            list = request.POST.getlist('tick')
            for x in list:
                save_tick(x, form.cleaned_data.get('lesson'))
            return json_response("OK",get_page(request))
    return json_response("ERROR")

@req
def ld_delete(request, lid):
    if request.method == "POST":
        teacher = request.user.teacher
        try:
            teacher.lessonday_set.get(pk=int(lid)).delete()
            return json_response("OK",get_page(request))
        except LessonDay.DoesNotExist:
            return json_response("NO SUCH LESSON DAY")
    return json_response("ERROR")