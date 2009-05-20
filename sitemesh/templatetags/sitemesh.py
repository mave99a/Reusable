from google.appengine.api import urlfetch
from google.appengine.api import memcache
from django import template
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import HttpResponse
import re
 
register = template.Library()
KEY_SITEMESH = 'SITEMESH_'

@register.tag
def loadurl(parser, token):
    param = token.contents.split()
    paramlen = len(param)
    
    if paramlen >=2:
        url = param[1]
    else: 
        url = ''
    
    if param >=3:
        exptime = int(param[2])
    else:
        exptime = 0
    
    return BlockNode(url, exptime)
    
def fetch_internal_url(url, context):
    resolved = resolve(url)   
    if resolved is None: 
        return ''
    view_func, args, kw = resolved
    
    if (hasattr(context, 'request')):
        request = context['request']
    else:
        request = HttpRequest()
        
    response = view_func(request, *args, **kw)
    return response.content

def is_extern_url(url):
    p = re.compile('http://', re.IGNORECASE)    
    return (p.match(url) is not None)
          

class BlockNode(template.Node): 
    def __init__(self, url, exptime):
        self.url = url
        self.exptime = exptime
        
    def render(self, context):   
        output = memcache.get(KEY_SITEMESH+self.url)
        
        if output is None: 
            if (is_extern_url(self.url)):
                result = urlfetch.fetch(self.url)            
                output = result.content
            else:
                output = fetch_internal_url(self.url, context)
            # add to cache
            memcache.add(KEY_SITEMESH+self.url, output, self.exptime)
        
        return output