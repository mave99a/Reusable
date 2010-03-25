import logging
from django import template
from django.template.loader import render_to_string
from django.http import HttpRequest
from taggable.models import Taggable

register = template.Library()

class ShowTagsNode(template.Node):
    def __init__(self, obj_ref, editable = False):
        self.obj_ref = template.Variable(obj_ref)
        self.editable = editable
        
    def render(self, context):
        obj = self.obj_ref.resolve(context)
        if obj is not None: 
            taggable = Taggable.get_taggable(obj)        
            return render_to_string('taggable/tags.html', {'taggable': taggable, 'target':obj, 'editable': self.editable }, context)
        return ''

def do_show_tags(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError("%r tag usage: { show_tags  object}" % tokens[0])
    return ShowTagsNode(tokens[1], False)

def do_show_tags_editable(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError("%r tag usage: { show_tags_editable  object}" % tokens[0])
    return ShowTagsNode(tokens[1], True)

register.tag('show_tags', do_show_tags)
register.tag('show_tags_editable', do_show_tags_editable)