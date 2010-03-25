from django import template
from renderhelpers.templatetags.conditional_tag_helper import condition_tag

register = template.Library()

@register.inclusion_tag('userbox.html', takes_context=True)
def authuserbox(context):
    return context

@register.tag
@condition_tag
def check_access(objectowner, request='request'):
    return request.authuser.user == objectowner
