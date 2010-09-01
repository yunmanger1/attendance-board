from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views_student.get', name="eplace_students_index"),
    url(r'^get/$', 'eplace.views_student.get', name="eplace_students_get"),
)

