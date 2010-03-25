import logging
from django import template
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.utils import simplejson


register = template.Library()

class UserImageNode(template.Node):
    def __init__(self, target_ref):
        self.target_ref = template.Variable(target_ref)
    
    def render(self, context):
        target = self.target_ref.resolve(context)
        userimage = simplejson.loads(target)
        output =''
        try:
           templatepath = 'userimage/%s.html' % userimage['type']      
           output = render_to_string(templatepath, userimage)
        except template.TemplateDoesNotExist: 
            output = '[err: template %s not found]' % templatepath
            logging.error('Render: template %s not found]' % templatepath)          
        
        return output

def do_userimage(parser, token):
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError("%r tag usage: { tag object}" % tokens[0])
    return UserImageNode(tokens[1])

register.tag('userimage', do_userimage)