from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^people/', include('people.urls')),
)