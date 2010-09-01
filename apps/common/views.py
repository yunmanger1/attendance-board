from django.utils.simplejson import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse

def get_url(request):    
    d= {}
    for k, v in request.GET.items():
        d.update({k:v})
    del d['urlname']
    try:
        url = reverse(request.GET['urlname'],None,kwargs=d)
    except:
        return HttpResponse("ERROR")
    return HttpResponse(url)