from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import simplejson

from urlparse import urlparse
from eplace.models import Teacher, Superviser, Dean

def get_page(request):
    url =  request.POST.get('getpage', request.GET.get('getpage', None))
#    print url
    if url is None:
        return ''
    view, args, kwargs = resolve(url)
#    print view, args, kwargs
#    return ''
    r = view(request, *args, **kwargs)
    d = simplejson.loads(r.content)
    return d['html']
        

def getval(lesson, val):
    for v, k, kk in settings.TICK_VALUES:
        if val == '+': return lesson.hours
        if k == val:
            return v
    return None

def json_response(m, html=''):
    json =simplejson.dumps({'m':m, 'html':html})
    return HttpResponse(json, mimetype="application/json")

def get_group_lessons(group):
    return group.lesson_set.all()

def is_teacher(user):
    if user.is_anonymous():
        return False
    t = Teacher.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False
    
def is_superviser(user):
    if user.is_anonymous():
        return False
    t = Superviser.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False

def is_dean(user):
    if user.is_anonymous():
        return False
    t = Dean.objects.filter(user=user)
    if (t.count() > 0):
        return True
    return False