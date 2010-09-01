from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views.index', name="eplace_index"),
    (r'^teacher/', include('eplace.urls_teacher')),
    (r'^student/', include('eplace.urls_student')),
    (r'^settings/', include('eplace.urls_settings')),
)

