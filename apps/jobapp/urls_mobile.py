from django.conf.urls.defaults import *
from django.conf import settings



urlpatterns = patterns('jobapp.views_mobile',                       
    url(r'^$', 'index', name='mobile_big'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'index', name='mobile_big'),
)
