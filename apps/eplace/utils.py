from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import simplejson

from urlparse import urlparse

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
