from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext

from eplace.models import is_teacher, is_dean, is_superviser
from eplace.forms import SettingsForm, get_default_settings


def index_teacher(request, template_name="eplace/teacher/index.html"):
    teacher = request.user.teacher
    c = RequestContext(request, {'teacher' : teacher, 'curpage': 'teachers'})
    return render_to_response(template_name, c)

def settings_teacher(request, template_name="eplace/teacher/settings.html"):
    teacher = request.user.teacher
    form = SettingsForm(initial=get_default_settings(request))
    c = RequestContext(request, {'form': form, 'teacher' : teacher, 'curpage': 'settings'})
    return render_to_response(template_name, c)

############## switches ###########################
def index_sw(f):
    def nf(request, *a, **kw):
        if (is_teacher(request.user)):
            return index_teacher(request, *a, **kw)
        return f(request, *a, **kw)
    return nf

def settings_sw(f):
    def nf(request, *a, **kw):
        if (is_teacher(request.user)):
            return settings_teacher(request, *a, **kw)
        return f(request, *a, **kw)
    return nf
############## switches ###########################

@index_sw
def index(request, template_name="eplace/home.html"):
    c = RequestContext(request, {})
    return render_to_response(template_name, c)

@settings_sw
def settings(request, template_name="eplace/home.html"):
    c = RequestContext(request, {})
    return render_to_response(template_name, c)
