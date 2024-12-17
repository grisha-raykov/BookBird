from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    nickname = forms.CharField(
        required=False,
        max_length=50,
    )
    birth_date = forms.DateField(
        required=False,
    )
    country = forms.CharField(
        required=False,
        max_length=100,
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
    class Meta:
        model = UserProfile
        fields = (
            "nickname",
            "birth_date",
            "country",
            "bio",
            "avatar",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
