import re

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User

from breakout.models import BreakoutSession

register = Library()

@register.simple_tag
def active(request, pattern):
    pattern = '^%s' % pattern
    if re.search(pattern, request.path):
        return 'active'
    return ''

# from http://www.djangosnippets.org/snippets/1609/
@register.filter
def sortby(sequence, attribute):
    # variation on dictsort using attribute access
    lst = list(sequence)
    lst.sort(key=lambda obj: getattr(obj,attribute))
    return lst


word_split_re = re.compile(r'(\s+)')

@register.filter
@stringfilter
def twitterize(text, autoescape=None):
    """Converts twitter usernames in plain text into clickable links."""
    text = force_unicode(text)
    text = re.sub(r'@([a-zA-Z0-9_]+)', r'<a href="http://twitter.com/\1" target="_blank">@\1</a>', text)
    text = re.sub(r'#([a-zA-Z0-9_]+)', r'<a href="http://twitter.com/search?q=%23\1" target="_blank">#\1</a>', text)
    return mark_safe(text)
twitterize.is_safe=True
twitterize.needs_autoescape = True

# from http://www.djangosnippets.org/snippets/661/
@register.filter
@stringfilter
def highlight(text, search_terms=None):
    if isinstance(search_terms, basestring):
        search_terms = [search_terms]
    
    search_terms = map(re.escape, search_terms)
    re_template = r"(%s)"
    expr = re.compile(re_template % "|".join(search_terms), re.I)
    inner_expr = re.compile('<a[^>]+?href="[^>]*?(%s)$' % "|".join(search_terms), re.I)
    matches = []
    
    def replace(match):
        span = match.span()
        if inner_expr.search(text, span[0]-100, span[1]):
            return match.group(0)
        matches.append(match)
        return '<span class="highlight">%s</span>' % (match.group(0), )
    
    highlighted = mark_safe(expr.sub(replace, text))
    count = len(matches)
    return highlighted

# http://www.djangosnippets.org/snippets/1685/
def location(request):
    location = {}
    current_site = Site.objects.get_current()
    location['site'] = current_site
    
    script_name = request.META['SCRIPT_NAME']
    location['script_name'] = script_name
    
    path = request.META['PATH_INFO']
    location['path'] = path
    
    url = 'http://%s%s%s' % (current_site, script_name, path)
    location['url'] = url
    
    return {'location': location}

# http://www.djangosnippets.org/snippets/1686/
@register.filter
def match(value, regex):
    """Usage: {% if value|match:"regex" %}"""
    return re.match(regex, value)

# TODO: This should be converted into a tag {% ifregistered %}
@register.filter
def is_registered(breakout_session, user):
    try:
        if breakout_session:
            return breakout_session.is_registered(user)
    except:
        pass
        # print "Bad user: %s" % user
    return False

# TODO: This should be converted into a tag {% ifregistered %}
@register.filter
def is_participating(breakout_session, user):
    try:
        if breakout_session:
            return breakout_session.is_participating(user)
    except:
        pass
        # print "Bad user: %s" % user
    return False
 
# @register.simple_tag
# def is_registered(request, breakout_session):
#     if not breakout_session:
#         return False
#     if not hasattr(request, user):
#         return False
#     return breakout_session.is_registered(request.user)
# 
# class IfRegisteredNode(Node):
#     def __init__(self, nodelist_true, nodelist_false, *varlist):
#         self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
#         self._last_seen = None
#         self._varlist = varlist
#         self._id = str(id(self))
# 
#     def render(self, context):
#         if 'forloop' in context and self._id not in context['forloop']:
#             self._last_seen = None
#             context['forloop'][self._id] = 1
#         try:
#             if self._varlist:
#                 # Consider multiple parameters.  This automatically behaves
#                 # like an OR evaluation of the multiple variables.
#                 compare_to = [var.resolve(context, True) for var in self._varlist]
#             else:
#                 compare_to = self.nodelist_true.render(context)
#         except VariableDoesNotExist:
#             compare_to = None
# 
#         if compare_to != self._last_seen:
#             firstloop = (self._last_seen == None)
#             self._last_seen = compare_to
#             content = self.nodelist_true.render(context)
#             return content
#         elif self.nodelist_false:
#             return self.nodelist_false.render(context)
#         return ''
# 
# def ifregistered(parser, token):
#     bits = token.contents.split()
#     nodelist_true = parser.parse(('else', 'endifregistered'))
#     token = parser.next_token()
#     if token.contents == 'else':
#         nodelist_false = parser.parse(('endifregistered',))
#         parser.delete_first_token()
#     else:
#         nodelist_false = NodeList()
#     values = [parser.compile_filter(bit) for bit in bits[1:]]
#     return IfRegisteredNode(nodelist_true, nodelist_false, *values)
# ifregistered = register.tag(ifregistered)
