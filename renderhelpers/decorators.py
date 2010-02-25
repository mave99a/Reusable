from django.utils import simplejson
from django.http import Http404, HttpResponse, HttpResponseRedirect


def AutoResponse(template=None, autoAjax=True, redirectBack=False):
    """
    Decorator for django views that automatically apply template for normal http request, 
    and response as JSON if it's an AJAX request. 
    
    If no template is provided, it will redirect to the location where 'returnurl' defined, 
    or if there is no 'returnurl' it try to redirect to the referrer URL. if no referer found 
    it will redirect to '/'
    
    """    
    def AutoResponseDecorator(view_func):
        def wrapper(request, *args, **kwargs):
            context = view_func(request, *args, **kwargs)
            
            if (autoAjax and request.is_ajax()):
                json = simplejson.dumps(context)
                return HttpResponse(json, mimetype='application/json')     
            
            if (template is None) or redirectBack:
                try:       
                    returnurl = request.REQUEST['returnurl']
                except:
                    returnurl = request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(returnurl)
            
            return render_to_response(
                            template, 
                            context, 
                            context_instance=RequestContext(request),
                        )            
        return wrapper
    return AutoResponseDecorator