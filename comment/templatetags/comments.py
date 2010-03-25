import logging
from django import template
from django.http import HttpRequest

from comment.views import new_comment

register = template.Library()

class CommentFormNode(template.Node):
    def __init__(self, target_ref):
        self.target_ref = template.Variable(target_ref)
    
    def render(self, context):
        target = self.target_ref.resolve(context)
        try: 
            request = context['request']
        except: 
            request = HttpRequest()
        return new_comment(request, target.key()).content

    

def do_comment_form(parser, token):
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise template.TemplateSyntaxError("%r tag usage: { tag for object}" % tokens[0])
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])
    return CommentFormNode(tokens[2])

register.tag('comment_form', do_comment_form)