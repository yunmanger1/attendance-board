from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'common.views.get_url', name="get_url"),
)

