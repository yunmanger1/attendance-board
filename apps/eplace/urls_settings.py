from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^teachers/$', 'eplace.views.settings', name="eplace_settings"),
    url(r'^save/$', 'eplace.views_settings.save', name="eplace_settings_save"),
    url(r'^get/$', 'eplace.views_settings.get', name="eplace_settings_get"),
)

