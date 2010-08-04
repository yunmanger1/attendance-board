from django.conf.urls.defaults import *
from django.conf import settings



urlpatterns = patterns('',
                       
#    url(r'^home/$', 'dailyjob_list', name='dailyjob_list'),
    (r'^daily/', include('jobapp.urls_daily')),
    (r'^stat/', include('jobapp.urls_stat')),
)
