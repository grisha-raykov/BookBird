from django import forms
from django.core.exceptions import ValidationError

from .models import Author
from .validators import AuthorValidator


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()

        # Validate birth date
        if birthdate := cleaned_data.get("birthdate"):
            try:
                year, month, day = AuthorValidator.validate_date(birthdate, "birthdate")
                cleaned_data["birth_year"] = year
                cleaned_data["birth_month"] = month
                cleaned_data["birth_day"] = day
            except ValidationError as e:
                self.add_error("birthdate", e)

        # Validate death date
        if deathdate := cleaned_data.get("deathdate"):
            try:
                year, month, day = AuthorValidator.validate_date(deathdate, "deathdate")
                cleaned_data["death_year"] = year
                cleaned_data["death_month"] = month
                cleaned_data["death_day"] = day
            except ValidationError as e:
                self.add_error("deathdate", e)

        return cleaned_data
