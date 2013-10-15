
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def fix_last_first(value):
    split = value.split(',')
    if len(split) == 1:
        return value
    elif len(split) == 2:
        l = [str.strip() for str in split]
        l.reverse()
        return ' '.join(l)

    return value

@register.filter
@stringfilter
def first_name(value):
    split = value.split(' ')
    if len(split) != 2:
        return value

    return split[0]
