from django import forms
from django.core.exceptions import ValidationError

from .models import Author
from .validators import AuthorValidator
from django.utils.translation import gettext_lazy as _


class AuthorAdminForm(forms.ModelForm):
    """Custom form for Author admin with enhanced validation"""

    transliterated_canonical_name = forms.CharField(
        required=False,
        label=_("Transliterated Canonical Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )

    transliterated_legal_name = forms.CharField(
        required=False,
        label=_("Transliterated Legal Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "vTextField"}),
    )

    class Meta:
        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-populate transliteration fields if they exist
            canonical_trans = self.instance.transliterations.filter(
                type="CANONICAL"
            ).first()
            if canonical_trans:
                self.fields[
                    "transliterated_canonical_name"
                ].initial = canonical_trans.transliterated_name
            legal_trans = self.instance.transliterations.filter(type="LEGAL").first()
            if legal_trans:
                self.fields[
                    "transliterated_legal_name"
                ].initial = legal_trans.transliterated_name

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
