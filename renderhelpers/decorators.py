from django.utils.decorators import wraps
from utils import AutoRendResponse

def method_adapter(func_decorator):
    """
        the decorator's decorator to adapt the view function decorator to be able to work in a class
        
        usage: 
            class View:
                @method_adapter(loginrequired)
                @method_adapter(cache_page(60*5))
                def view_method(request):
                   pass
    """
    def adaptorwrapper(unbound_method):
        def wrapper(self_or_class, *args, **kwargs):
            def f(*args, **kwargs):
                return unbound_method(self_or_class, *args, **kwargs)
            return func_decorator(f)(*args, **kwargs)
        return wrapper
    return adaptorwrapper
    
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
            return AutoRendResponse(request, template, autoAjax, redirectBack, context)
        return wrapper
    return AutoResponseDecorator