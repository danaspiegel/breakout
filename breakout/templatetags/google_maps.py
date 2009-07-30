from django import template
from django.conf import settings
from django.template import Library
from django.template import RequestContext
from django.template import resolve_variable

register = Library()

INCLUDE_TEMPLATE = '<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s" type="text/javascript"></script>' % (settings.GOOGLE_MAPS_API_KEY, )

class GMapScriptNode (template.Node):
    def __init__(self):
        pass        
    def render (self, context):
        return INCLUDE_TEMPLATE

def do_gmap_script(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("La etiqueta no requiere argumentos" % token.contents[0])
    return GMapScriptNode()

do_gmap_script = register.tag('gmap_script', do_gmap_script)