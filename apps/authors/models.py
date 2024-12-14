from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from BookBird.mixins import DateComponentsMixin
from apps.languages.models import Language


# Create your models here.
class Author(models.Model, DateComponentsMixin):
    canonical_name = models.TextField(
        blank=False,
        null=False,
        help_text="Canonical name of the author",
    )

    legal_name = models.TextField(
        blank=True,
        null=True,
        help_text="Legal name of the author. Should be Family Name, Given Name",
    )

    last_name = models.TextField(
        blank=True,
        null=True,
        db_index=True,
        help_text=_("Family name used for sorting (derived from canonical name)"),
    )

    birthplace = models.TextField(
        blank=True,
        null=True,
        help_text="Place of birth of the author. Should contain city, state, and country",
    )

    birth_year = models.IntegerField(
        blank=True,
        null=True,
    )

    birth_month = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )

    birth_day = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31),
        ],
    )

    death_year = models.IntegerField(
        blank=True,
        null=True,
    )

    death_month = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text=_("Month of death (1-12) if known"),
    )

    death_day = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text=_("Day of death (1-31) if known"),
    )

    birthdate = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_("Date format: YYYY or YYYY-MM or YYYY-MM-DD"),
    )

    deathdate = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_("Date format: YYYY or YYYY-MM or YYYY-MM-DD"),
    )

    language = models.ForeignKey(
        Language,
        blank=False,
        null=True,
        on_delete=models.PROTECT,  # Prevent language deletion if authors exist
        related_name="authors",
        help_text=_("Primary language of the author's works"),
    )

    wikipedia_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL of the author's Wikipedia page"),
    )
    imdb_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL of the author's IMDb page"),
    )
    views = models.PositiveIntegerField(
        default=0,
        help_text=_("Total number of author page views"),
    )

    annual_views = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of views in the last year"),
    )

    popularity_score = models.PositiveIntegerField(
        default=0,
        help_text=_("Calculated popularity score (0-100)"),
    )

    image_url = models.URLField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional notes about the author. Supports markdown"),
    )

    def clean(self) -> None:
        """Parse display dates into components"""
        if self.birthdate:
            try:
                self.birth_year, self.birth_month, self.birth_day = (
                    self.parse_date_display(self.birthdate)
                )
            except ValidationError as e:
                raise ValidationError({"birthdate_display": e})

        if self.deathdate:
            try:
                self.death_year, self.death_month, self.death_day = (
                    self.parse_date_display(self.deathdate)
                )
            except ValidationError as e:
                raise ValidationError({"deathdate_display": e})

        super().clean()

    def update_popularity_score(self) -> None:
        """
        Calculate author popularity based on:
        - Total views (50% weight)
        - Annual views (50% weight)

        The score is calculated as follows:
        1. Total views component (50%):
           - The total views are capped at 10,000.
           - The score contribution from total views is calculated as
             (min(self.views, 10000) * 50) // 10000.
           - This ensures that the maximum contribution from total views is 50.

        2. Annual views component (50%):
           - The annual views are capped at 1,000.
           - The score contribution from annual views is calculated as
             (min(self.annual_views, 1000) * 50) // 1000.
           - This ensures that the maximum contribution from annual views is 50.

        The final popularity score is the sum of the contributions from total views
        and annual views, ensuring a balanced and fair scoring system.

        The views and annual_views are capped to prevent the score from being
        disproportionately influenced by extremely high view counts, maintaining
        a balanced and fair scoring system.
        """
        base_score = 0

        # Total views component (50%)
        if self.views > 0:
            base_score += (min(self.views, 10000) * 50) // 10000

        # Annual views component (50%)
        if self.annual_views > 0:
            base_score += (min(self.annual_views, 1000) * 50) // 1000

        self.popularity_score = base_score
        self.save(update_fields=["popularity_score"])

    def save(self, *args, **kwargs) -> None:
        """
        Generate last_name from canonical_name if not provided.
        Called automatically on model save.
        """
        if self.canonical_name and not self.last_name:
            # Take the last word from canonical name as family name
            self.last_name = self.canonical_name.split()[-1]

        if self.birth_year:
            if all(x is not None for x in [self.birth_month, self.birth_day]):
                self.birthdate = (
                    f"{self.birth_year:04d}-{self.birth_month:02d}-{self.birth_day:02d}"
                )
            else:
                self.birthdate = f"{self.birth_year:04d}"
        else:
            self.birthdate = ""

            # Handle death date
        if self.death_year:
            if all(x is not None for x in [self.death_month, self.death_day]):
                self.deathdate = (
                    f"{self.death_year:04d}-{self.death_month:02d}-{self.death_day:02d}"
                )
            else:
                self.deathdate = f"{self.death_year:04d}"
        else:
            self.deathdate = ""
        super().save(*args, **kwargs)