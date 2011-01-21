from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'eplace.views_groups.index', name="eplace_groups_index"),
    url(r'^group(?P<gid>\d+)/$','eplace.views_groups.group', name="eplace_groups_get"),
#    url(r'^lesson(?P<lid>\d+)/gen/$','eplace.views_teachers.generate', name="eplace_teacher_generate_ld"),
#    url(r'^ticksave/$','eplace.views_teachers.tick_save', name="eplace_teacher_tick_save"),    
#    url(r'^ld(?P<lid>\d+)/delete/$','eplace.views_teachers.ld_delete', name="eplace_teacher_ld_delete"),    
)

