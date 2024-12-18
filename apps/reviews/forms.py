from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={"class": "rating-input"}),
        required=True,
        error_messages={
            "required": _("Please select a rating"),
        },
    )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": _("Write your review here..."),
            }
        ),
        required=True,
        error_messages={
            "required": _("Please write your review"),
        },
    )

    class Meta:
        model = Review
        fields = ["rating", "text"]

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if len(text.strip()) < 10:
            raise forms.ValidationError(_("Review must be at least 10 characters long"))
        return text
