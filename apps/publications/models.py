from django.db import models
from django.utils.translation import gettext_lazy as _


from django.core.exceptions import ValidationError
from BookBird.mixins import DateComponentsMixin
from apps.core.models import ISFDBBase, TransliterationBase
from apps.publications.choices import PublicationFormat, PublicationType


class Publication(ISFDBBase, models.Model, DateComponentsMixin):
    """Model representing specific publications of works"""

    title = models.TextField(
        blank=False,
        null=False,
        help_text=_("Title of the publication"),
    )

    authors = models.ManyToManyField(
        "authors.Author",
        through="PublicationAuthor",
        related_name="publications",
        help_text=_("Author/s of the publication"),
    )

    isfdb_tag = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("ISFDB tag for this publication"),
    )

    publication_date = models.CharField(
        max_length=12,
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
        help_text=_("Number of pages in the publication"),
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
        max_length=100,
        blank=True,
        null=True,
        help_text=_("ISBN-10 or ISBN-13"),
    )

    image_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL of the publication's cover image"),
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

    series_number = models.CharField(
        max_length=255,
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
            except ValidationError:
                raise ValidationError(
                    {
                        "publication_date": ValidationError(
                            _("Invalid date format. Use YYYY, YYYY-MM, or YYYY-MM-DD"),
                            code="invalid_date",
                        )
                    }
                )
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
        super().clean()


class PublicationSeriesTransliteration(TransliterationBase):
    """Model for storing romanized transliterations of publication series names"""

    publication_series = models.ForeignKey(
        "PublicationSeries",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Publication Series"),
        help_text=_("The original publication series this transliteration belongs to"),
    )

    class Meta:
        verbose_name = _("Publication Series Transliteration")
        verbose_name_plural = _("Publication Series Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text


class PublisherTransliteration(TransliterationBase):
    """Model for storing romanized transliterations of publisher names"""

    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.CASCADE,
        related_name="transliterations",
        verbose_name=_("Publisher"),
        help_text=_("The original publisher this transliteration belongs to"),
    )

    class Meta:
        verbose_name = _("Publisher Transliteration")
        verbose_name_plural = _("Publisher Transliterations")
        ordering = ["transliterated_text"]

    def __str__(self):
        return self.transliterated_text


class PublicationAuthor(models.Model):
    """Model for Publication-Author relationship"""

    author = models.ForeignKey(
        "authors.Author",
        on_delete=models.CASCADE,
        related_name="publication_relationships",
        help_text=_("Author of the publication"),
    )

    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
        related_name="author_relationships",
        help_text=_("Publication by this author"),
    )

    class Meta:
        verbose_name = _("Publication Author")
        verbose_name_plural = _("Publication Authors")
        unique_together = ["author", "publication"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["publication"]),
        ]

    def __str__(self):
        return f"{self.author} - {self.publication}"


class PublicationTitle(ISFDBBase):
    """Model representing the relationship between titles and publications"""

    title = models.ForeignKey(
        "titles.Title",
        on_delete=models.CASCADE,
        related_name="publication_appearances",
        help_text=_("Title appearing in this publication"),
    )

    publication = models.ForeignKey(
        "publications.Publication",
        on_delete=models.CASCADE,
        related_name="contained_titles",
        help_text=_("Publication containing this title"),
    )

    page = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Page number where the title appears in the publication"),
    )

    class Meta:
        verbose_name = _("Publication Title")
        verbose_name_plural = _("Publication Titles")
        ordering = ["publication", "page"]
        indexes = [
            models.Index(fields=["isfdb_id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["publication"]),
        ]

    def __str__(self):
        page_info = f" (p. {self.page})" if self.page else ""
        return f"{self.title.title} in {self.publication}{page_info}"
