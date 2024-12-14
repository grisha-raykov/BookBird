from datetime import date
from typing import Optional, Tuple
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DateComponentsMixin:
    """Mixin for handling date components"""

    def parse_date_display(
        self, display_value: str
    ) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """
        Parse a display date string into year, month, day components.

        Args:
            display_value: Date string in YYYY, YYYY-MM or YYYY-MM-DD format

        Returns:
            Tuple of (year, month, day) where month and day may be None

        Raises:
            ValidationError: If date format is invalid
        """
        try:
            parts = display_value.split("-")
            if len(parts) == 1:  # YYYY
                year = int(parts[0])
                return year, None, None
            elif len(parts) == 2:  # YYYY-MM
                year, month = map(int, parts)
                return year, month, None
            elif len(parts) == 3:  # YYYY-MM-DD
                year, month, day = map(int, parts)
                # Validate full date
                date(year, month, day)
                return year, month, day
            raise ValueError(_("Invalid date format"))
        except (ValueError, TypeError):
            raise ValidationError(_("Invalid date format"))
