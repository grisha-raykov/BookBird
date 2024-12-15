from django import forms
from django.core.exceptions import ValidationError

from .models import Title
from .validators import TitleValidator


class TitleAdminForm(forms.ModelForm):
    """Custom form for Title admin with enhanced validation"""

    class Meta:
        model = Title
        fields = "__all__"

    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()

        # Validate in form for better user feedback
        TitleValidator.validate_hierarchy(
            cleaned_data.get("parent_title"),
            cleaned_data.get("is_canonical"),
        )

        TitleValidator.validate_content_flags(
            cleaned_data.get("type"),
            cleaned_data.get("is_graphic"),
        )

        if first_pub_date := cleaned_data.get("first_pub_date"):
            try:
                year, month, day = TitleValidator.validate_date(
                    first_pub_date,
                    "first_pub_date",
                )
                cleaned_data["first_pub_year"] = year
                cleaned_data["first_pub_month"] = month
                cleaned_data["first_pub_day"] = day
            except ValidationError as e:
                self.add_error("first_pub_date", e)

        return cleaned_data
