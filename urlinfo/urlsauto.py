from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^urlinfo/', include('urlinfo.urls')),
)