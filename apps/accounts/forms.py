from django.utils import timezone
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email"),
            }
        ),
    )
    nickname = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your nickname"),
            }
        ),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": _("Enter your birth date"),
            }
        ),
    )
    country = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your country"),
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "nickname",
            "birth_date",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
            if field in self.errors:
                self.fields[field].widget.attrs.update(
                    {"class": "form-control is-invalid"}
                )

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if nickname and UserProfile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError(_("This nickname is already taken."))
        return nickname

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError(_("Birth date cannot be in the future."))
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.profile.nickname = self.cleaned_data["nickname"]
            user.profile.birth_date = self.cleaned_data["birth_date"]
            user.profile.country = self.cleaned_data["country"]
            user.profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    nickname = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Choose a nickname"),
            }
        ),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )
    country = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Your country"),
            }
        ),
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": _("Tell us about yourself"),
            }
        ),
    )
    avatar = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": _("URL to your profile picture"),
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = (
            "nickname",
            "birth_date",
            "country",
            "bio",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field in self.errors:
                field.widget.attrs["class"] = "form-control is-invalid"

    def clean(self):
        cleaned_data = super().clean()
        if avatar_url := cleaned_data.get("avatar"):
            if not avatar_url.startswith(("http://", "https://")):
                self.add_error("avatar", _("Please enter a valid URL"))
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username"),
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password"),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        password1 = self.cleaned_data.get("new_password1")
        if password1 and password2 and password1 != password2:
            self.add_error("new_password2", _("The two password fields didn't match."))
        return password2
