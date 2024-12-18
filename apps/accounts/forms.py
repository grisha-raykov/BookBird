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
                "placeholder": "Enter your email",
            }
        ),
    )
    nickname = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your nickname",
            }
        ),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your birth date",
            }
        ),
    )
    country = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your country",
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
                    "placeholder": f'Enter your {field.replace("_", " ")}',
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
                "placeholder": _("Your date of birth"),
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
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        nickname = self.cleaned_data.get("nickname")
        birth_date = self.cleaned_data.get("birth_date")

        if username and password:
            # Check if username exists
            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    _("Username does not exist."), code="invalid_username"
                )

            # Try to authenticate
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                # Username exists but password is wrong
                raise forms.ValidationError(
                    _("Incorrect password."), code="invalid_password"
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    _("This account is inactive."), code="inactive"
                )

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with that email already exists."))

        if nickname and UserProfile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError(_("A user with that nickname already exists."))

        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError(_("Birth date cannot be in the future."))

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.errors:
            for field in self.fields.values():
                field.widget.attrs["class"] = "form-control is-invalid"


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn’t match."))
        return password2
