from django.core.exceptions import ValidationError


class AuthorValidator:
    """Validators for Author model"""

    @classmethod
    def validate_date(cls, date_string: str, field_name: str):
        """Validate and parse date string"""
        from BookBird.mixins import DateComponentsMixin

        if not date_string:
            return None, None, None

        try:
            return DateComponentsMixin().parse_date_display(date_string, field_name)
        except ValidationError as e:
            raise ValidationError({field_name: e})
