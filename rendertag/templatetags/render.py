from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from parseargshelper import parse_args_kwargs_and_as_var

register = template.Library()
BASE_PATH = 'components'

class RenderObjectNode(template.Node):
    def __init__(self, object_ref, template_name=None, as_var = None):
        self.object_ref = template.Variable(object_ref)
        self.template_name = template_name
        self.as_var = as_var
        
    def render(self, context):
        try: 
            object = self.object_ref.resolve(context)
        except:
            object = None
        templatepath = self.template_name
        if object is None:
            output = ''
        else: 
            if (object.__class__.__name__ != 'dict') and hasattr(object, '__len__'): 
                templatepath = BASE_PATH + '/list.html'
                templatecontext = {'objects': object}
            elif not templatepath:  
                if hasattr(object, 'templatename'):         # check if it's a class which provide template name
                    templatepath = BASE_PATH + '/' + object.templatename + '.html'
                else:              
                    try: # dictionary lookup
                        templatepath = BASE_PATH + '/'  + object['templatename']+ '.html'
                    except (TypeError, AttributeError, KeyError):
                        templatepath = BASE_PATH + '/' + object.__class__.__name__.lower() + '.html'
                templatecontext = {'object': object}
                
            try:        
                context.push()
                output = render_to_string(templatepath, templatecontext, context)
                context.pop()
            except template.TemplateDoesNotExist: 
                output = '[err: template %s not found]' % templatepath
            
            output = mark_safe(output)
             
        return output
    
def do_render_object(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r requires at least 1 arguments" % bits[0]
    else: 
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])
        return RenderObjectNode(args[0], template_name=kwargs.get("template"), as_var = as_var)

register.tag('render', do_render_object)