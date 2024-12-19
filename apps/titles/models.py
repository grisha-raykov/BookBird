from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from BookBird.mixins import DateComponentsMixin
from apps.core.models import Note, ISFDBBase, StatsBase, TransliterationBase
from apps.languages.models import Language
from apps.titles.choices import TitleType, StoryLength, AuthorRole
from apps.titles.validators import TitleValidator


class Title(ISFDBBase, StatsBase, DateComponentsMixin):
    title = models.TextField(
        blank=False,
        null=False,
        help_text="Title of the work",
    )

    language = models.ForeignKey(
        Language,
        null=True,
        on_delete=models.PROTECT,
        related_name="titles",
        help_text=_("Primary language of this title"),
    )

    authors = models.ManyToManyField(
        "authors.Author",
        through="AuthorTitle",
        related_name="titles",
        help_text=_("Authors of the work"),
    )

    first_pub_date = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Date of first publication in the format YYYY-MM-DD, YYYY-MM, or YYYY",
    )
    first_pub_year = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("First publication year"),
    )
    first_pub_month = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("First publication month"),
    )
    first_pub_day = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("First publication day"),
    )

    parent_title = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="variant_titles",
        help_text=_(
            "Parent canonical title. If null, this is a canonical title; if set, this is a variant title"
        ),
    )

    is_canonical = models.BooleanField(
        default=True,
        null=True,
        help_text=_(
            "Is this canonical title or a variant title?",
        ),
    )

    is_graphic = models.BooleanField(
        default=False,
        null=True,
        help_text=_(
            "Indicates if this title is graphic in nature. Note: Cover art and interior art are not considered graphic"
        ),
    )

    is_novelization = models.BooleanField(
        default=False,
        null=True,
        help_text=_(
            "Indicates if this title is a novelization from a movie, TV show, etc."
        ),
    )

    is_juvenile = models.BooleanField(
        default=False,
        null=True,
        help_text=_(
            "Indicates if this title is aimed at the juvenile/young adult audience"
        ),
    )

    is_non_genre = models.BooleanField(
        default=False,
        null=True,
        help_text=_("Indicates if this title is not speculative fiction"),
    )

    content_indicator = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_(
            "Content indicator for omnibuses (e.g. '1,2+ss' indicates parts 1, 2 plus short stories)"
        ),
    )

    story_length = models.CharField(
        max_length=20,
        choices=StoryLength.choices,
        blank=True,
        null=True,
        help_text=_("Length category for short fiction titles"),
    )

    type = models.CharField(
        max_length=20,
        choices=TitleType.choices,
        default=TitleType.NOVEL,
        help_text=_("Type of the title (e.g. Novel, Collection, Anthology)"),
    )

    synopsis = models.TextField(
        blank=True,
        null=True,
        help_text=_("Synopsis of the work"),
    )

    series_position = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Position within the series (e.g. 1, 1.5, 3)"),
    )

    series = models.ForeignKey(
        "Series",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
        help_text=_("Series this title belongs to"),
    )

    notes = GenericRelation(Note)

    def clean(self):
        TitleValidator.validate_hierarchy(
            self.parent_title,
            self.is_canonical,
        )

        TitleValidator.validate_content_flags(
            self.type,
            self.is_graphic,
        )

        if self.first_pub_date:
            self.first_pub_year, self.first_pub_month, self.first_pub_day = (
                TitleValidator.validate_date(
                    self.first_pub_date,
                    "first_pub_date",
                )
            )
        if self.type == TitleType.SHORTFICTION and not self.story_length:
            raise ValidationError(
                {
                    "story_length": _(
                        "Story length is required for short fiction titles"
                    ),
                }
            )
        elif self.type != TitleType.SHORTFICTION and self.story_length:
            raise ValidationError(
                {
                    "story_length": _(
                        "Story length should only be set for short fiction titles"
                    )
                }
            )

        super().clean()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class TitleTransliteration(TransliterationBase):
    """Model for storing romanized transliterations of titles"""

    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Title"),
        help_text=_("The original title this transliteration belongs to"),
    )

    class Meta:
        verbose_name = _("Title Transliteration")
        verbose_name_plural = _("Title Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text


class Series(models.Model):
    """Model for book series with hierarchical structure support"""

    title = models.CharField(
        max_length=255,
        help_text=_("Name of the series"),
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subseries",
        help_text=_("Parent series if this is a subseries"),
    )

    series_parent_position = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Position within the parent series (e.g. 1, 1.5, 3)"),
    )

    series_note = models.TextField(
        null=True,
        blank=True,
        help_text=_("Additional notes about this series"),
    )
    isfdb_id = models.IntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text=_("ISFDB ID for this series"),
    )

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError

        # Prevent self-referential parent
        if self.parent == self:
            raise ValidationError(
                {
                    "parent": _(
                        "A series cannot be its own parent",
                    ),
                }
            )

        if self.parent and self.series_parent_position is None:
            raise ValidationError(
                {
                    "series_parent_position": _(
                        "Position is required when parent series is set"
                    )
                }
            )

    def get_ancestors(self):
        """Get all ancestor series in order"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))

    class Meta:
        verbose_name = _("Series")
        verbose_name_plural = _("Series")
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["series_parent_position"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["isfdb_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "series_parent_position"],
                name="unique_series_position",
            )
        ]


class SeriesTransliteration(models.Model):
    """Model for storing romanized transliterations of series names"""

    series = models.ForeignKey(
        "Series",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Series"),
        help_text=_("The original series this transliteration belongs to"),
    )

    transliterated_text = models.TextField(
        verbose_name=_("Romanized Text"),
        help_text=_("Romanized version of the series name"),
    )

    class Meta:
        verbose_name = _("Series Transliteration")
        verbose_name_plural = _("Series Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text


class AuthorTitle(models.Model):
    """Intermediary model for Author-Title relationship with role information"""

    author = models.ForeignKey(
        "authors.Author",
        on_delete=models.CASCADE,
        related_name="title_relationships",
        help_text=_("Author of the title"),
    )

    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name="author_relationships",
        help_text=_("Title authored by this author"),
    )

    role = models.IntegerField(
        choices=AuthorRole.choices,
        default=AuthorRole.CANONICAL,
        help_text=_("Role of the author for this title"),
    )

    class Meta:
        verbose_name = _("Author-Title Relationship")
        verbose_name_plural = _("Author-Title Relationships")
        unique_together = ["author", "title", "role"]
        ordering = ["role", "author__last_name"]
        indexes = [
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.author} - {self.title} ({self.get_role_display()})"
