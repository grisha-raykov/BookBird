from django import template

register = template.Library()


@register.inclusion_tag("publications/includes/publication_cover.html")
def publication_cover(publication_appearances):
    """Render publication cover image if available"""
    first_pub = publication_appearances.first() if publication_appearances else None
    return {
        "publication": first_pub.publication if first_pub else None,
    }


@register.inclusion_tag("publications/includes/publication_year.html")
def publication_year(publication_appearances):
    """Render publication year if available"""
    first_pub = publication_appearances.first() if publication_appearances else None
    if first_pub and first_pub.publication.publication_date:
        year = first_pub.publication.publication_date[:4]
        return {"year": year if year != "0000" else None}
    return {"year": None}


@register.inclusion_tag("publications/includes/publication_details.html")
def publication_details(title):
    """Render publication details including cover and date"""
    first_pub = (
        title.publication_appearances.first()
        if title.publication_appearances.exists()
        else None
    )
    return {
        "publication": first_pub.publication if first_pub else None,
        "title": title,
    }


@register.simple_tag
def get_valid_publication_date(publication_appearances):
    """Get first valid publication date"""
    first_pub = publication_appearances.first()
    if first_pub and first_pub.publication.publication_date:
        year = first_pub.publication.publication_date[:4]
        return year if year != "0000" else None
    return None
