from django.conf.urls.defaults import *
from django.conf import settings



urlpatterns = patterns('jobapp.views_stat',                       
    url(r'^$', 'stat_home', name='stat_home'),
    url(r'^dailyjob/(?P<id>\d+)/$', 'stat_dailyjob', name='stat_dailyjob'),
)
