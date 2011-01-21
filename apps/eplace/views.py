from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext

from eplace.utils import is_teacher, is_dean, is_superviser
from eplace.forms import SettingsForm, get_default_settings


############### switches ###########################
#def index_sw(f):
#    def nf(request, *a, **kw):
#        if (is_teacher(request.user)):
#            return index_teacher(request, *a, **kw)
#        return f(request, *a, **kw)
#    return nf
#
#def settings_sw(f):
#    def nf(request, *a, **kw):
#        if (is_teacher(request.user)):
#            return settings_teacher(request, *a, **kw)
#        return f(request, *a, **kw)
#    return nf
############### switches ###########################
#
def index(request, template_name="eplace/home.html"):
    c = RequestContext(request, {})
    return render_to_response(template_name, c)
#
#@settings_sw
#def settings(request, template_name="eplace/home.html"):
#    c = RequestContext(request, {})
#    return render_to_response(template_name, c)
