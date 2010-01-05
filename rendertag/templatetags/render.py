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
        context.push()
        try: 
            object = self.object_ref.resolve(context)
        except:
            object = None
        
        if self.template_name:     
            try:
                templatepath = template.Variable(self.template_name).resolve(context)
            except: 
                templatepath = self.template_name
        else:
            templatepath = None
            
        if object is None:
            output = ''
        else:                 
            if (object.__class__.__name__ != 'dict') and hasattr(object, '__len__'): 
                templatecontext = {'objects': object, 
                                   'template_name': templatepath}  # save the previous template for list 
                templatepath = BASE_PATH + '/list.html'
            else: 
                if templatepath is None:  
                    templatepath = BASE_PATH + '/' + object.__class__.__name__.lower() + '.html'
                
                templatecontext = {'object': object}
                
            try:        
                output = render_to_string(templatepath, templatecontext)
            except template.TemplateDoesNotExist: 
                output = '[err: template %s not found]' % templatepath

        output = mark_safe(output)
        context.pop()
        return output
    
def do_render_object(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r requires at least 1 arguments" % bits[0]
    else: 
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])
        return RenderObjectNode(args[0], template_name=kwargs.get("template"), as_var = as_var)

register.tag('render', do_render_object)