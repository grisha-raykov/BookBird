from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """Model representing a language with ISO code and names"""

    code = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-z]{2,3}$",
                message=_("3 letter ISO 639-2 language code"),
            ),
        ],
        help_text=_("ISO 639-2 language code (e.g. 'eng', 'bul')"),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text=_("Language name in English (e.g. 'English', 'Bulgarian')"),
    )

    native_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[MinLengthValidator(2)],
        help_text=_("Language name in its native form (e.g. 'English', 'Български')"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("language")
        verbose_name_plural = _("languages")
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name}"
