from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class ReadingList(models.Model):
    LIST_TYPES = [
        ("read", _("Read")),
        ("currently_reading", _("Currently Reading")),
        ("to_read", _("Want to Read")),
        ("custom", _("Custom List")),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reading_lists"
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("List Name"),
    )
    list_type = models.CharField(
        max_length=20,
        choices=LIST_TYPES,
        default="custom",
    )
    is_default = models.BooleanField(
        default=False,
        help_text=_(
            "Indicates if this is a default system list",
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Reading List")
        verbose_name_plural = _("Reading Lists")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "list_type"],
                condition=models.Q(is_default=True),
                name="unique_default_list_type",
            )
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.name}"


class ListItem(models.Model):
    reading_list = models.ForeignKey(
        ReadingList, on_delete=models.CASCADE, related_name="items"
    )
    publication = models.ForeignKey(
        "publications.Publication",
        on_delete=models.CASCADE,
        related_name="list_entries",
    )
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    class Meta:
        ordering = ["-added_at"]
        unique_together = ["reading_list", "publication"]


@receiver(post_save, sender=User)
def create_default_lists(sender, instance, created, **kwargs):
    """Create default reading lists for new users"""
    if created:
        default_lists = [
            ("read", _("Read")),
            ("currently_reading", _("Currently Reading")),
            ("to_read", _("Want to Read")),
        ]
        for list_type, name in default_lists:
            ReadingList.objects.create(
                user=instance, name=name, list_type=list_type, is_default=True
            )
