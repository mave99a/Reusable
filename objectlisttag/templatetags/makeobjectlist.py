'''
makeobjectlist tag

<TODO>

'''

import logging
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.paginator  import Paginator, InvalidPage
from renderhelpers.templatetags.parseargshelper import parse_args_kwargs_and_as_var

register = template.Library()

class MakeObjectListNode(template.Node):
    def __init__(self, object_ref, as_var, paginate_by, addtion_filter):
        self.object_ref = template.Variable(object_ref)
        self.as_var = as_var
        try: 
            self.paginate_by = int(paginate_by)
        except: 
            self.paginate_by = 10
            
        self.addtion_filter = addtion_filter
            
    def render(self, context):
        try: 
            object = self.object_ref.resolve(context)
        except:
            object = None
        
        if self.as_var is None:
            self.as_var = 'object_list'
        
        if self.addtion_filter is not None: 
            queryset = eval("object." + self.addtion_filter)
        else:
            queryset = object
            
        paginator = Paginator(queryset, self.paginate_by,  allow_empty_first_page=True)
        
        request = context['request']
        page = request.GET.get('page', 1)
            
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                page_number = 1

        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            page_obj = paginator.page(1)
            
        context[self.as_var] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return ''
        
    
def do_make_object_list(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r requires at least 1 arguments" % bits[0]
    else: 
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])
        return MakeObjectListNode(args[0], 
                                paginate_by = kwargs.get("paginate_by"),
                                addtion_filter = kwargs.get("addtion_filter"),
                                as_var = as_var)

register.tag('makeobjectlist', do_make_object_list)

