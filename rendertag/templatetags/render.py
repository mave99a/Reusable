from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()
BASE_PATH = 'components'

class RenderObjectNode(template.Node):
    def __init__(self, object_ref, template_name=None):
        self.object_ref = template.Variable(object_ref)
        self.template_name = template_name
        
    def render(self, context):
        object = self.object_ref.resolve(context)
        output = ''
        templatepath = self.template_name
        if object is None:
            pass
        else: 
            if not templatepath:  
                if hasattr(object, 'templatename'):         # check if it's a class which provide template name
                    templatepath = BASE_PATH + '/' + object.templatename + '.html'
                else:              
                    try: # dictionary lookup
                        templatepath = BASE_PATH + '/'  + object['templatename']+ '.html'
                    except (TypeError, AttributeError, KeyError):
                        templatepath = BASE_PATH + '/' + object.__class__.__name__.lower() + '.html'
                
            try:        
                output = render_to_string(templatepath, {'objects':object, 'object': object})
            except template.TemplateDoesNotExist: 
                output = '[err: template %s not found]' % templatepath
            
            output = mark_safe(output)
             
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