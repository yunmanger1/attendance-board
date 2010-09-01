from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views.index', name="eplace_teacher_index"),
    url(r'^subject(?P<sid>\d+)/group(?P<gid>\d+)/$','eplace.views_teachers.subject', name="eplace_teacher_subject_group"),
    url(r'^subject(?P<sid>\d+)/group(?P<gid>\d+)/gen/$','eplace.views_teachers.generate', name="eplace_teacher_generate_ld"),
    url(r'^ticksave/$','eplace.views_teachers.tick_save', name="eplace_teacher_tick_save"),    
    url(r'^ld(?P<lid>\d+)/delete/$','eplace.views_teachers.ld_delete', name="eplace_teacher_ld_delete"),    
)

