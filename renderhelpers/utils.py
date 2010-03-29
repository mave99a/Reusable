from django.utils import simplejson
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def AutoRendResponse(request, template=None, autoAjax=True, redirectBack=False, context=None):
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