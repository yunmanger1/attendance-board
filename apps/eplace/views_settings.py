from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings

from eplace.models import is_teacher, is_dean, is_superviser
from eplace.models import Subject, Group, LessonDay, Tick
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
def save(request, template_name="eplace/teacher/settings_form.html"):
    if request.method == "POST":
        f = SettingsForm(request.POST)
        if f.is_valid():
            try:
                f.save(request.user)
                c = RequestContext(request, {'form': SettingsForm(initial=get_default_settings(request))})
                return json_response("OK", render_to_string(template_name, c))
            except:
                import traceback
                traceback.print_exc()
                return json_response("ERROR SAVING")
        else:
            return json_response("ERROR FORM")
    return json_response("ERROR")

@req
def get(request, template_name="eplace/teacher/settings_form.html"):
    c = RequestContext(request, {'form': SettingsForm(initial=get_default_settings(request))})
    if request.method == "POST":
        return json_response("OK", render_to_string(template_name, c))
    return json_response("ERROR")
