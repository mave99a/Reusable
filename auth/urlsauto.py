from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^auth/', include('auth.urls')),
)