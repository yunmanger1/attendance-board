from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views_student.get', name="eplace_students_index"),
    url(r'^(?P<id>\d+)/$', 'eplace.views_student.student', name="eplace_students_student"),
    url(r'^get/$', 'eplace.views_student.get', name="eplace_students_get"),
)

