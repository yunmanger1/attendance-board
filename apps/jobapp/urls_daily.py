from django.conf.urls.defaults import *
from django.conf import settings



urlpatterns = patterns('jobapp.views',
                       
    url(r'^$', 'dailyjob_list', name='dailyjob_list'),
    url(r'^add/$', 'dailyjob_add', name='dailyjob_add'),
    url(r'^delete/(?P<id>\d+)/$', 'dailyjob_delete', name='dailyjob_delete'),
    url(r'^toggle/(?P<id>\d+)/$', 'dailyjob_toggle', name='dailyjob_toggle'),
    url(r'^tickarch/(?P<id>\d+)/$', 'dailyjob_tickarch', name="dailyjob_tickarch"),
    url(r'^done/(?P<id>\d+)/$', 'dailyjob_done', name="dailyjob_done_adv"),
    url(r'^done/(?P<id>\d+)/(?P<tid>\d+)/$', 'dailyjob_done', name="dailyjob_done_edit"),
    url(r'^done/(?P<id>\d+)/today/$', 'dailyjob_done', {'date':'today'}, name="dailyjob_done"),
    url(r'^done/(?P<id>\d+)/n/(?P<n>\d+)/$', 'dailyjob_done', {'date':'today'}, name="dailyjob_done_n"),
)
