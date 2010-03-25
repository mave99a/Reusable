from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^(?P<id>\d+)/(?P<obj>\w+)/$', show_user), 
    (r'^(?P<id>\d+)/$', show_user), 
    # my 
    (r'^me/$', show_myhome), 
    (r'^settings/$', show_settings),
    (r'^settings/image/$', show_settings_profileimage),
    (r'^settings/services/$', show_settings_linkedservices),    
    (r'^$', list_user), 
    (r'^(?P<filter>\w+)/$', list_user),
    )