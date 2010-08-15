"""
Single Sign On Middleware
"""
import string
import time

from django.conf import settings
from django.contrib.auth import authenticate, login

class SingleSignOnMiddleware(object):
    
    def process_request(self, request):
        token     = request.GET.get('token', False)
        username        = request.GET.get('user', False)
        if token and username:
            user = authenticate(username=username, password=token)
            if user is not None:
                if user.is_active:
                    login(request, user)
        return None 
