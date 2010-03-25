from functools import update_wrapper, wraps
from django.utils.http import urlquote
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from views import login

def login_required(view_function):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    if the view is called from an AJAX request, it will not redirect, and only 
    return JSON error data
    """
    def login_required_wrapper(request, *args, **kw):
        if request.authuser.is_authenticated():
            return view_function(request, *args, **kw)
        else:
            if request.is_ajax(): 
                json = simplejson.dumps({ 'success': False, 'not_authenticated': True })
                return HttpResponse(json, mimetype='application/json')  
                          
            login_url = reverse(login)
            path = urlquote(request.get_full_path())
            return HttpResponseRedirect('%s?returnpath=%s' % (login_url, path))
            
    return wraps(view_function)(login_required_wrapper)

def superuser_required(view_function):
    """
    Decorator for views that checks that the user is logged in and is superuser, otherwise it throw 404
    and direct to a 404 page. 
    """
    def superuser_required_wrapper(request, *args, **kw):
        if request.authuser.is_authenticated():
            return view_function(request, *args, **kw)
        else:
            raise Http404('Page not found!')
        
    return wraps(view_function)(superuser_required_wrapper)    