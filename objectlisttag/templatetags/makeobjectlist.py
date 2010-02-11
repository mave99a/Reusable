'''
makeobjectlist tag

<TODO>

'''

import logging
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.paginator  import Paginator, InvalidPage
from rendertag.templatetags.parseargshelper import parse_args_kwargs_and_as_var

register = template.Library()

class MakeObjectListNode(template.Node):
    def __init__(self, object_ref, as_var = 'object_list',):
        self.object_ref = template.Variable(object_ref)
        self.as_var = as_var
            
    def render(self, context):
        try: 
            object = self.object_ref.resolve(context)
        except:
            object = None
        
        if self.as_var is None:
            self.as_var = 'object_list'
        
        queryset = eval("object.order('-mtime')")    
        paginator = Paginator(queryset, 3,  allow_empty_first_page=True)
        page_obj = paginator.page(1)
            
        context[self.as_var] = page_obj.object_list
        return ''
        
    
def do_make_object_list(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r requires at least 1 arguments" % bits[0]
    else: 
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])
        return MakeObjectListNode(args[0], 
                                as_var = as_var)

register.tag('makeobjectlist', do_make_object_list)

