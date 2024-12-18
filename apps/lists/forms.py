from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ReadingList


from django.utils.text import slugify


class ReadingListForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter list name"),
            }
        ),
    )

    class Meta:
        model = ReadingList
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            # Slugify the name to ensure valid characters
            slugified_name = slugify(name)
            if not slugified_name:
                raise forms.ValidationError(
                    _("List name must contain at least one letter or number")
                )
            return name
        return name
