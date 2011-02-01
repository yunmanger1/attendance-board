import sys
import os
import site


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

dir = '/opt/envs/atboard/lib/python2.5/site-packages'
site.addsitedir(dir)
sys.path.insert(0, PROJECT_ROOT)
sys.path.append(dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'atboard.settings'
  
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
