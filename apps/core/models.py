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


class TransliterationBase(models.Model):
    """Abstract base model for all transliteration models"""

    transliterated_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Romanized Text"),
        help_text=_("Romanized version of the original text"),
    )

    class Meta:
        abstract = True
        ordering = ["transliterated_text"]


class ISFDBBase(models.Model):
    """Abstract base model for ISFDB-linked models"""

    isfdb_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text=_("ISFDB ID"),
        db_index=True,
    )

    class Meta:
        abstract = True


class StatsBase(models.Model):
    """Abstract base model for models with view statistics"""

    views = models.PositiveIntegerField(
        default=0,
        help_text=_("Total number of page views"),
    )
    annual_views = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of views in the last year"),
    )
    popularity_score = models.PositiveIntegerField(
        default=0,
        help_text=_("Calculated popularity score"),
    )

    class Meta:
        abstract = True
