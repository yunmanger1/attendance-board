from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^index/$', 'eplace.views.index', name="eplace_index"),
    (r'^teacher/', include('eplace.urls_teacher')),
    (r'^student/', include('eplace.urls_student')),
    (r'^groups/', include('eplace.urls_groups')),
    (r'^settings/', include('eplace.urls_settings')),
)

