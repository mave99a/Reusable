from django.utils.decorators import wraps
from utils import AutoRendResponse
    
def AutoResponse(template=None, autoAjax=True, redirectBack=False):
    """
    Decorator for django views that automatically apply template for normal http request, 
    and response as JSON if it's an AJAX request. 
    
    If no template is provided, it will redirect to the location where 'returnurl' defined, 
    or if there is no 'returnurl' it try to redirect to the referrer URL. if no referer found 
    it will redirect to '/'
    
    """    
    def AutoResponseDecorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            context = view_func(request, *args, **kwargs)     
            return AutoRendResponse(request, template, autoAjax, redirectBack, context)
        return wrapper
    return AutoResponseDecorator