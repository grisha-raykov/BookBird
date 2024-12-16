from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    """Generic notes model that can be linked to any other model"""

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text=_("Type of object this note belongs to"),
    )
    object_id = models.PositiveIntegerField(
        help_text=_("ID of the related object"),
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    note_text = models.TextField(
        help_text=_("Note content. Supports markdown"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When this note was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("When this note was last updated"),
    )

    note_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("Type/category of the note"),
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["note_type"]),
        ]

    def __str__(self):
        return f"Note for {self.content_object}: {self.note_text[:50]}..."
