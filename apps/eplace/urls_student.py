from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views_student.get', name="eplace_students_index"),
    url(r'^(?P<id>\d+)/$', 'eplace.views_student.student', name="eplace_students_student"),
    url(r'^(?P<sid>\d+)/lesson(?P<lid>\d+)/$', 'eplace.views_student.student_lesson', name="eplace_students_student_lesson"),
    url(r'^lesson(?P<id>\d+)/$', 'eplace.views_student.lesson', name="eplace_students_lesson"),
    url(r'^get/$', 'eplace.views_student.get', name="eplace_students_get"),
)

