from django.db import models
from django.utils.translation import gettext_lazy as _


from django.core.exceptions import ValidationError
from BookBird.mixins import DateComponentsMixin
from apps.publications.choices import PublicationFormat, PublicationType


class Publication(models.Model, DateComponentsMixin):
    """Model representing specific publications of works"""

    title = models.TextField(
        blank=False,
        null=False,
        help_text=_("Title of the publication"),
    )

    isfdb_tag = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("ISFDB tag for this publication"),
    )

    publication_date = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_("Publication date in YYYY-MM-DD, YYYY-MM, or YYYY format"),
    )

    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="publications",
        help_text=_("Publisher of this publication"),
    )

    pages = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Number of pages"),
    )

    format = models.CharField(
        max_length=50,
        choices=PublicationFormat.choices,
        blank=True,
        null=True,
        help_text=_("Format/binding type of the publication"),
    )

    ctype = models.CharField(
        max_length=32,
        choices=PublicationType.choices,
        blank=True,
        null=True,
        help_text=_("Type of the publication"),
        db_index=True,
    )

    isbn = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        help_text=_("ISBN-10 or ISBN-13"),
    )

    price = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("Main price of the publication"),
    )

    publication_series = models.ForeignKey(
        "PublicationSeries",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publications",
        help_text=_("Publication series this belongs to"),
    )

    series_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Position within the publication series"),
    )

    catalog_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Catalog ID of the publication"),
    )

    isfdb_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text=_("ISFDB publication ID"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")
        ordering = ["publication_date", "title"]
        indexes = [
            models.Index(fields=["isbn"]),
            models.Index(fields=["publication_date"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-series_number"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.publisher}, {self.publication_date})"

    def clean(self):
        """Validate publication data"""
        if self.publication_date:
            try:
                self.parse_date_display(self.publication_date, "publication_date")
            except ValidationError as e:
                raise ValidationError({"publication_date": e})
        super().clean()


class Publisher(models.Model):
    name = models.TextField(
        blank=False,
        null=False,
        help_text=_("Name of the publisher"),
    )

    slug = models.SlugField(
        max_length=255,
        blank=True,
        unique=True,
        help_text=_("Slug for the publisher"),
    )

    website = models.URLField(
        blank=True,
        null=True,
        help_text=_("Publisher's website URL"),
    )

    isfdb_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text=_("ISFDB publisher ID"),
        db_index=True,
    )

    def __str__(self):
        return self.name

    def clean(self):
        """Validate publisher data"""
        super().clean()


class PublicationSeries(models.Model):
    """Model representing publication series (e.g. SF Masterworks)"""

    name = models.TextField(
        blank=False, null=False, help_text=_("Name of the publication series")
    )

    slug = models.SlugField(
        max_length=255,
        blank=True,
        unique=True,
        help_text=_("URL-friendly version of the name"),
    )

    isfdb_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        unique=True,
        help_text=_("ISFDB publication series ID"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Publication Series")
        verbose_name_plural = _("Publication Series")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Validate publication series data"""
        super().clean()


class PublicationSeriesTransliteration(models.Model):
    """Model for storing romanized transliterations of publication series names"""

    publication_series = models.ForeignKey(
        "PublicationSeries",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Publication Series"),
        help_text=_("The original publication series this transliteration belongs to"),
    )

    transliterated_text = models.TextField(
        verbose_name=_("Romanized Text"),
        help_text=_("Romanized version of the publication series name"),
    )

    class Meta:
        verbose_name = _("Publication Series Transliteration")
        verbose_name_plural = _("Publication Series Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text


class PublisherTransliteration(models.Model):
    """Model for storing romanized transliterations of publisher names"""

    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Publisher"),
        help_text=_("The original publisher this transliteration belongs to"),
    )

    transliterated_text = models.TextField(
        verbose_name=_("Romanized Text"),
        help_text=_("Romanized version of the publisher name"),
    )

    class Meta:
        verbose_name = _("Publisher Transliteration")
        verbose_name_plural = _("Publisher Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text
