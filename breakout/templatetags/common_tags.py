import re

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.template import Library
from django.template.defaultfilters import stringfilter

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
    words = word_split_re.split(force_unicode(text))
    for i, word in enumerate(words):
        if word.startswith('@') and len(word) > 1:
            # Make URL we want to point to.
            words[i] = mark_safe('<a href="http://twitter.com/%s">%s</a>' % (word[1:], word))
    return u''.join(words)
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