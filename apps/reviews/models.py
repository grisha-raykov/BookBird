from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )
    title = models.ForeignKey(
        "titles.Title",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Title"),
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name=_(
            "Rating",
        ),
    )
    text = models.TextField(
        verbose_name=_("Review Text"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        unique_together = ["user", "title"]

    def __str__(self):
        return f"{self.user}'s review of {self.title}"
