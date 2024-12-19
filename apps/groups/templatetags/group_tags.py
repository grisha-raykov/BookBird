from django import template

register = template.Library()


@register.filter
def is_member(group, user):
    return group.members.filter(id=user.id).exists()
