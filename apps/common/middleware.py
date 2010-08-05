from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import activate 
    
from common.models import UserField

class UserLanguageMiddleware(object):

    def process_request(self, request):
        lang = request.session.get('django_language','ru')
        if request.user.is_authenticated() and request.session.get('django_language',None) is None:
            try:
                l = UserField.objects.get(user=request.user, key="default_language")
                lang = l.value
            except UserField.DoesNotExist:
                pass
        activate(lang)
        return None