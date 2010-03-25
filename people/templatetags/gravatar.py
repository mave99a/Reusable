'''
    Gravatar template tag
    
    The Gravatar URL rule is defined here: 
    http://en.gravatar.com/site/implement/url
'''
from django import template
from django.utils.html import escape
from django.contrib.auth.models import User

import urllib, hashlib

register = template.Library()

def gravatar(email, size=80, default_img = None):   
    gravatar_url = "http://www.gravatar.com/avatar/%s?" % hashlib.md5(email).hexdigest()
    if default_img is None: 
       default_img = 'identicon' 
    gravatar_url += urllib.urlencode({'d': default_img, 's':str(size)})
    return gravatar_url

register.simple_tag(gravatar)
