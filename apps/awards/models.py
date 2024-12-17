# apps/awards/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import ISFDBBase

from django.core.validators import MinValueValidator, MaxValueValidator


class AwardLevel(models.IntegerChoices):
    WIN = 1, _("Win")
    NOMINATION = 9, _("Nomination")
    NO_WINNER_INSUFFICIENT_VOTES = 71, _("No Winner - Insufficient Votes")
    NOT_ON_BALLOT_INSUFFICIENT_NOMINATIONS = (
        72,
        _("Not on ballot -- Insufficient Nominations"),
    )
    NO_AWARD_GIVEN = 73, _("No Award Given This Year")
    WITHDRAWN = 81, _("Withdrawn")
    WITHDRAWN_NOMINATION_DECLINED = 82, _("Withdrawn - Nomination Declined")
    WITHDRAWN_CONFLICT_OF_INTEREST = 83, _("Withdrawn - Conflict of Interest")
    WITHDRAWN_PRIOR_PUBLICATION = (
        84,
        _("Withdrawn - Official Publication in a Previous Year"),
    )
    WITHDRAWN_INELIGIBLE = 85, _("Withdrawn - Ineligible")
    FINALISTS = 90, _("Finalists")
    MADE_FIRST_BALLOT = 91, _("Made First Ballot")
    PRELIMINARY_NOMINEE = 92, _("Preliminary Nominee")
    HONORABLE_MENTION = 93, _("Honorable Mention")
    EARLY_SUBMISSION = 98, _("Early Submission")
    NOMINATION_BELOW_CUTOFF = 99, _("Nomination Below Cutoff")


class Award(ISFDBBase):
    """Model representing individual awards given to titles, authors, etc."""

    title = models.TextField(
        null=True,
        help_text=_(
            "Title as recorded when award was given. For non-title awards like 'Best Artist', contains 'untitled'"
        ),
    )

    author = models.TextField(
        blank=True,
        null=True,
        help_text=_(
            "Author(s) as recorded when award was given, multiple authors separated by '+'"
        ),
    )

    year = models.TextField(
        blank=True,
        null=True,
        help_text=_("Year the award was given"),
    )

    level = models.PositiveIntegerField(
        blank=True,
        null=True,
        choices=AwardLevel.choices,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text=_(
            "1-70: Poll position, 1: Win, 9: Nomination, "
            "71-99: Special statuses like withdrawn/finalists"
        ),
    )

    movie_title = models.TextField(
        null=True,
        blank=True,
        help_text=_("IMDB movie title for movie-related awards"),
    )

    type = models.ForeignKey(
        "AwardType",
        on_delete=models.CASCADE,
        related_name="awards",
        help_text=_("Award type (e.g. Hugo, Nebula)"),
    )

    category = models.ForeignKey(
        "AwardCategory",
        on_delete=models.CASCADE,
        related_name="awards",
        help_text=_("Award category (e.g. Best Novel)"),
    )

    class Meta:
        verbose_name = _("Award")
        verbose_name_plural = _("Awards")
        ordering = ["type", "year", "category", "level"]
        indexes = [
            models.Index(fields=["isfdb_id"]),
            models.Index(fields=["type", "year"]),
            models.Index(fields=["category", "year"]),
            models.Index(fields=["level"]),
        ]

    def __str__(self):
        return f"{self.type.name} {self.year} - {self.category.name}"

    SPECIAL_LEVELS = {
        71: _("No Winner -- Insufficient Votes"),
        72: _("Not on ballot -- Insufficient Nominations"),
        73: _("No Award Given This Year"),
        81: _("Withdrawn"),
        82: _("Withdrawn - Nomination Declined"),
        83: _("Withdrawn - Conflict of Interest"),
        84: _("Withdrawn - Official Publication in a Previous Year"),
        85: _("Withdrawn - Ineligible"),
        90: _("Finalists"),
        91: _("Made First Ballot"),
        92: _("Preliminary Nominee"),
        93: _("Honorable Mention"),
        98: _("Early Submission"),
        99: _("Nomination Below Cutoff"),
    }


class AwardType(ISFDBBase):
    """Model representing types of awards (Hugo, Nebula, etc.)"""

    code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        help_text=_("Short code identifying the award type"),
        db_index=True,
    )

    name = models.TextField(
        help_text=_("Full name of the award type"),
    )

    short_name = models.TextField(
        blank=True,
        null=True,
        help_text=_("Short/common name of the award"),
    )

    by = models.TextField(
        blank=True,
        null=True,
        help_text=_("Organization giving the award"),
    )

    for_what = models.TextField(
        blank=True,
        null=True,
        help_text=_(
            "What the award is given for"
        ),  # 'for' is a reserved word in Python
    )

    wikipedia_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL of award's Wikipedia page"),
    )

    is_poll = models.BooleanField(
        default=False,
        help_text=_("Indicates if this is a poll rather than a juried award"),
    )

    is_non_genre = models.BooleanField(
        default=False,
        help_text=_("Indicates if this is not a speculative fiction award"),
    )

    class Meta:
        verbose_name = _("Main Award")
        verbose_name_plural = _("Main Awards")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["isfdb_id"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()


class AwardCategory(ISFDBBase):
    """Model representing award categories (Best Novel, Best Artist, etc.)"""

    name = models.TextField(
        null=True,
        help_text=_("Name of the award category"),
    )

    type = models.ForeignKey(
        "AwardType",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        help_text=_("Award type this category belongs to"),
    )

    order = models.PositiveIntegerField(
        null=True,
        help_text=_("Display order within award type"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Award Category")
        verbose_name_plural = _("Award Categories")
        ordering = ["type", "order", "name"]
        indexes = [
            models.Index(fields=["isfdb_id"]),
            models.Index(fields=["type", "order"]),
        ]

    def __str__(self):
        return f"{self.type.name} - {self.name}"


class TitleAward(ISFDBBase):
    """Model representing the relationship between titles and awards"""

    award = models.ForeignKey(
        "Award",
        on_delete=models.CASCADE,
        null=True,
        related_name="title_awards",
        help_text=_("Award given to this title"),
    )

    title = models.ForeignKey(
        "titles.Title",
        on_delete=models.CASCADE,
        null=True,
        related_name="awards",
        help_text=_("Title that received the award"),
    )

    class Meta:
        verbose_name = _("Title Award")
        verbose_name_plural = _("Title Awards")
        ordering = ["award__type", "award__year"]
        indexes = [
            models.Index(fields=["isfdb_id"]),
            models.Index(fields=["award"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title.title} - {self.award}"
