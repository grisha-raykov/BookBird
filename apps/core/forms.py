from django import forms
from django.utils.translation import gettext_lazy as _


class GlobalSearchForm(forms.Form):
    q = forms.CharField(
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Search books, authors, series, ISBN"),
                "type": "search",
            }
        ),
        error_messages={
            "min_length": _("Please enter at least 3 characters."),
            "required": _("Please enter a search term."),
        },
    )

    def clean_q(self):
        query = self.cleaned_data["q"]
        if len(query.strip()) < 3:
            raise forms.ValidationError(_("Please enter at least 3 characters."))
        return query
