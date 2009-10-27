from django import template
from django.template.loader import render_to_string

register = template.Library()
BASE_PATH = 'objects'

class RenderObjectNode(template.Node):
    def __init__(self, object_name, template_name=None):
        self.object_name = object_name
        self.template_name = template_name
        
    def render(self, context):
        object = context[self.object_name]
        output = ''
        template = self.template_name
        if object is None:
            pass
        else: 
            if not template:  
                if hasattr(object, 'templatename'):         # check if it's a class which provide template name
                    template = BASE_PATH + '/' + object.templatename + '.html'
                else:              
                    try: # dictionary lookup
                        template = BASE_PATH + '/'  + object['templatename']+ '.html'
                    except (TypeError, AttributeError, KeyError):
                        template = BASE_PATH + '/' + object.__class__.__name__.lower() + '.html'
                
            try:        
                output = render_to_string(template, {'objects':object, 'object': object}, context)
            except: 
                pass
             
        return output
    
def do_render_object(parser, token):
    bits = token.split_contents()
    if len(bits) == 2:
        return RenderObjectNode(bits[1])
    elif len(bits) == 3:
        return RenderObjectNode(bits[1], bits[2])
    else:
        raise template.TemplateSyntaxError, "%r requires one or two arguments" % bits[0]

register.tag('render', do_render_object)