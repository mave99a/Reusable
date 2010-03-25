from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^comment/', include('comment.urls')),
)