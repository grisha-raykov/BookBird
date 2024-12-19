from django import template

register = template.Library()


@register.filter
def map(sequence, attr):
    """Get attribute from sequence of objects"""
    return [getattr(item, attr) for item in sequence]
