from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TitleValidator:
    """Validators for Title model"""

    @classmethod
    def validate_hierarchy(cls, parent_title, is_canonical):
        """Validate title parent-child relationships"""
        if not is_canonical and not parent_title:
            raise ValidationError(
                {
                    "parent_title": _("Non-canonical titles must have a parent title"),
                }
            )

        if parent_title and parent_title.parent_title:
            raise ValidationError(
                _(
                    "Variant titles cannot have variant titles - only one level of nesting is allowed"
                )
            )

    @classmethod
    def validate_content_flags(cls, type, is_graphic):
        """Validate content flags based on title type"""
        from .choices import TitleType

        if is_graphic and type in [TitleType.COVERART, TitleType.INTERIORART]:
            raise ValidationError(
                {
                    "is_graphic": _(
                        "Cover art and interior art cannot be marked as graphic"
                    )
                }
            )

    @classmethod
    def validate_date(cls, date_string, field_name):
        """Validate and parse date string"""
        from BookBird.mixins import DateComponentsMixin

        if not date_string:
            return None, None, None

        try:
            return DateComponentsMixin().parse_date_display(date_string, field_name)
        except ValidationError as e:
            raise ValidationError({field_name: e})
