# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from user import *

def login(request):
    AuthMethods = [FacebookUser, GoogleUser]
    try: 
        returnpath = request.REQUEST['returnpath']
    except: 
        returnpath = request.get_full_path()
    return render_to_response('auth/login.html',
                              {'authmethods': AuthMethods,
                               'returnpath': returnpath,
                              },
                              context_instance=RequestContext(request))