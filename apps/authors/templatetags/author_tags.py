from django import template

register = template.Library()


@register.filter
def filter_title_awards(titles):
    """Filter titles that have awards"""
    return [
        title for title in titles if hasattr(title, "awards") and title.awards.exists()
    ]


@register.filter
def filter_wins(titles):
    """Filter titles that have won awards (level=1)"""
    return [title for title in titles if title.awards.filter(award__level=1).exists()]


@register.filter
def filter_nominations(titles):
    """Filter titles that have nominations (level=9)"""
    return [title for title in titles if title.awards.filter(award__level=9).exists()]
