import sys,os

sys.path.append('/home/german/distr/django-trunk')
sys.path.append('/home/german/work')
os.environ['DJANGO_SETTINGS_MODULE'] = 'watchme.settings'
  
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
