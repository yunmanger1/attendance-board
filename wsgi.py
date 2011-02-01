import sys,os

os.environ['DJANGO_SETTINGS_MODULE'] = 'atboard.settings'
  
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
