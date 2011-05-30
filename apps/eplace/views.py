from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request, template_name="eplace/home.html"):
    c = RequestContext(request, {})
    return render_to_response(template_name, c)
