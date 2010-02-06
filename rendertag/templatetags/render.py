'''
RederTag

listtemplate can be used for customize list in the situation that simple UL/Table won't work. user can specify a 
template to generate the list itself. two context varible is passed in.

  objects:  the object list
  template_name:  the customized template name specified from user code

A sample listtemplate is like following:

    <ul>
        {% for object in objects %}
        <li>{% render object template=template_name%}</li>
        {% endfor %}
    </ul>

'''

import logging
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from parseargshelper import parse_args_kwargs_and_as_var

register = template.Library()
BASE_PATH = 'components'

def renderhelper(object, templatepath, listtemplate=None, template_postfix=None, context_instance=None):
    ''' Render object or object list '''
    if object is None:
        return ''
 
    if (object.__class__.__name__ != 'dict') and hasattr(object, '__len__'): 
        if listtemplate is None:
            output =''
            isTable = False;
            hasDetected = False;
            for item in object:
                t = renderhelper(item, templatepath, template_postfix=template_postfix, context_instance = context_instance)
                #
                #  detect if we should use <Table> or <ul> based on the list item
                #
                if not hasDetected:
                    if t.lstrip()[:3].upper() == '<TD':
                        isTable = True;
                    hasDetected = True;
                
                # generate list automatically
                if isTable:
                    output += '<tr>%s</tr>' % t
                else:
                    output += '<li>%s</li>' % t
            if isTable:
                output = '<table>%s</table>' % output
            else:
                output = '<ul>%s</ul>' % output
                
            return output        
        else:
            # render the list itself with a template file
            templatecontext = {'objects': object, 
                               'template_name': templatepath}  # save the previous template for list 
            templatepath = listtemplate
            logging.debug('Render: using list template')
    else: 
        if templatepath is None:  
            templatepath = BASE_PATH + '/' + object.__class__.__name__.lower()
            if template_postfix is not None:
                templatepath += '_' + template_postfix.lower()
            templatepath += '.html'
            logging.debug('Render: using default template %s' % templatepath)
            
        templatecontext = {'object': object}
        
    try:        
        output = render_to_string(templatepath, templatecontext, context_instance)
    except template.TemplateDoesNotExist: 
        output = '[err: template %s not found]' % templatepath
        logging.error('Render: template %s not found]' % templatepath)    

    return mark_safe(output)

class RenderObjectNode(template.Node):
    def __init__(self, object_ref, template_name=None, as_var = None, listtemplate=None, template_postfix=None):
        logging.debug('Render: object=%s, template_name=%s' % (object_ref, template_name))
        self.object_ref = template.Variable(object_ref)
        self.template_name = template_name
        self.as_var = as_var
        self.listtemplate = listtemplate
        self.template_postfix = template_postfix
            
    def render(self, context):
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

        return renderhelper(object, 
                            templatepath, 
                            listtemplate=self.listtemplate,
                            template_postfix = self.template_postfix,
                            context_instance = context)
    
def do_render_object(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "%r requires at least 1 arguments" % bits[0]
    else: 
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])
        return RenderObjectNode(args[0], 
                                template_name=kwargs.get("template"), 
                                template_postfix =kwargs.get("templatetype"),
                                listtemplate=kwargs.get("listtemplate"),
                                as_var = as_var)

register.tag('render', do_render_object)