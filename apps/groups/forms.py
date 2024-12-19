from dal import autocomplete
from django import forms
from .models import ReadingGroup, GroupDiscussion, DiscussionComment
from django.utils.translation import gettext_lazy as _


class ReadingGroupForm(forms.ModelForm):
    class Meta:
        model = ReadingGroup
        fields = ["name", "description", "is_private", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Group name"),
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": _("Description"),
                },
            ),
            "is_private": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                },
            ),
            "image": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Image URL"),
                },
            ),
        }


class GroupDiscussionForm(forms.ModelForm):
    class Meta:
        model = GroupDiscussion
        fields = ["topic", "title"]
        widgets = {
            "topic": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Discussion topic"),
                }
            ),
            "title": autocomplete.ModelSelect2(
                url="titles:ta",
                attrs={
                    "class": "form-control",
                    "data-placeholder": _("Search for a title..."),
                    "data-minimum-input-length": 2,
                },
            ),
        }


class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _("Add a comment..."),
                },
            ),
        }


class GroupSearchForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=ReadingGroup.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="groups:group-autocomplete",
            attrs={
                "data-placeholder": "Search groups...",
                "data-minimum-input-length": 2,
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = ReadingGroup.objects.all()
