from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from views import *

urlpatterns = patterns('',
    (r'^gpr/(.*)$',gpr),
        
    (r'^gpages/(.*)$', gpages), 
    (r'^glinks/(.*)$', glinks), 
    (r'^livepages/(.*)$', livepages), 
    (r'^livelinks/(.*)$', livelinks), 
    (r'^baidupages/(.*)$', baidupages),
    (r'^baidulinks/(.*)$', baidulinks), 
    (r'^ypages/(.*)$', ypages), 
    (r'^ylinks/(.*)$', ylinks),

    (r'^delicious/(.*)$', delicious),
    (r'^reddit/(.*)$', reddit),
    #(r'^digg/(.*)$', digg),
    (r'^stumbleupon/(.*)$', stumbleupon),

    (r'^w3chtml/(.*)$', w3chtml),
    (r'^w3ccss/(.*)$', w3ccss),
       
    (r'^whois/(.*)$', whois),    
)
