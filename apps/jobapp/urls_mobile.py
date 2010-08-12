from django.conf.urls.defaults import *
from django.conf import settings



urlpatterns = patterns('jobapp.views_mobile',                       
    url(r'^$', 'index', name='mobile_big'),
)
