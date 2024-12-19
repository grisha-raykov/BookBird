from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Nickname"),
        help_text=_("Your preferred display name"),
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Birth Date"),
        help_text=_("Your date of birth"),
    )

    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Country"),
        help_text=_("Your country of residence"),
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Biography"),
        help_text=_("Tell us about yourself"),
    )

    avatar = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Avatar URL"),
        help_text=_("URL to your profile picture"),
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["user__username"]
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError(_("Birth date cannot be in the future"))

        if self.birth_date and self.birth_date.year < 1900:
            raise ValidationError(
                {"birth_date": _("Birth date year cannot be before 1900.")}
            )
        if self.nickname:
            # Check for forbidden words
            forbidden_words = ["admin", "root", "system"]  # Example list
            if self.nickname.lower() in forbidden_words:
                raise ValidationError({"nickname": _("This nickname is not allowed.")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
