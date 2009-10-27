from django.template import add_to_builtins
# register our tag as default, so we don't need to use "{%load ...%}" all the time
add_to_builtins('rendertag.templatetags.render')
