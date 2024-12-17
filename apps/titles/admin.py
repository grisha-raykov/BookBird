from django.contrib import admin
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.titles.inlines import (
    VariantTitleInline,
    TitleTransliterationInline,
    SeriesTitleInline,
    AuthorTitleInline,
    SeriesTransliterationInline,
)
from .choices import TitleType
from .forms import TitleAdminForm
from .models import Title, Series, AuthorTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    form = TitleAdminForm
    inlines = [VariantTitleInline, TitleTransliterationInline, AuthorTitleInline]

    list_display = [
        "title",
        "type",
        "language",
        "is_canonical",
        "first_pub_date",
        "display_authors",
    ]
    list_select_related = [
        "language",
        "parent_title",
        "series",
    ]
    list_per_page = 20

    list_filter = [
        "type",
        "language",
        "is_canonical",
        "is_graphic",
        ("is_juvenile", admin.BooleanFieldListFilter),
        "is_non_genre",
        "is_novelization",
    ]

    search_fields = [
        "title",
        "language__name",
        "transliterations__transliterated_text",
        "parent_title__title",
    ]

    readonly_fields = [
        "id",
        "first_pub_year",
        "first_pub_month",
        "first_pub_day",
        "series_info",
    ]

    autocomplete_fields = [
        "parent_title",
        "language",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "title",
                    "type",
                    "story_length",
                    "language",
                    "first_pub_date",
                )
            },
        ),
        (
            _("Title Relationships"),
            {
                "fields": (
                    "parent_title",
                    "is_canonical",
                ),
                "description": _("Parent title and variant titles relationship"),
            },
        ),
        (
            _("Series Information"),
            {
                "fields": (
                    "series",
                    "series_position",
                    "series_info",
                ),
                "description": _("Series this title belongs to"),
            },
        ),
        (
            _("Content Flags"),
            {
                "fields": (
                    "is_graphic",
                    "is_juvenile",
                    "is_non_genre",
                    "is_novelization",
                )
            },
        ),
        (
            _("Additional Info"),
            {"fields": ("content_indicator",)},
        ),
    ]

    def series_info(self, obj):
        """Display series information with hierarchy"""
        if not obj.series:
            return _("Not part of a series")

        current_series = obj.series
        series_chain = []

        while current_series:
            position = ""
            if current_series == obj.series:
                position = f" (#{obj.series_position})" if obj.series_position else ""
            elif current_series.series_parent_position:
                position = f" (#{current_series.series_parent_position})"

            series_chain.append(
                format_html(
                    '<a href="{}">{}</a>{}',
                    reverse("admin:titles_series_change", args=[current_series.pk]),
                    current_series.title,
                    position,
                )
            )
            current_series = current_series.parent

        return format_html(" → ".join(reversed(series_chain)))

    series_info.short_description = _("Series Hierarchy")

    def get_queryset(self, request):
        """Optimize querysets with prefetch_related for variants"""
        return (
            super()
            .get_queryset(request)
            .select_related(
                "language",
                "parent_title",
                "series",
            )
            .prefetch_related(
                "variant_titles",
                "transliterations",
                Prefetch(
                    "author_relationships",
                    queryset=AuthorTitle.objects.select_related("author").only(
                        "author__canonical_name", "role", "title_id", "author_id"
                    ),
                ),
            )
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make story_length required for short fiction
        if obj and obj.type == TitleType.SHORTFICTION:
            form.base_fields["story_length"].required = True
        return form

    def display_authors(self, obj):
        """Display authors in list view"""
        authors = obj.author_relationships.all()
        return ", ".join(f"{ar.author.canonical_name}" for ar in authors)

    display_authors.short_description = _("Authors")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesTitleInline, SeriesTransliterationInline]
    list_display = ["title", "parent", "series_parent_position"]
    search_fields = ["title"]
    list_select_related = ["parent"]
    readonly_fields = ["isfdb_id", "subseries_list"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "title",
                    "isfdb_id",
                    (
                        "parent",
                        "series_parent_position",
                    ),
                    "series_note",
                    "subseries_list",
                )
            },
        ),
    ]

    def get_queryset(self, request):
        """Optimize queryset for series admin"""
        return (
            super()
            .get_queryset(request)
            .select_related("parent")
            .prefetch_related("titles")
        )

    def subseries_list(self, obj):
        """Display nested subseries recursively"""

        def render_subseries(series, level=0):
            result = []
            subseries = series.subseries.select_related("parent").order_by(
                "series_parent_position"
            )

            for sub in subseries:
                indent = "&nbsp;" * (level * 4)
                result.append(
                    f'<div style="margin-left: {level * 20}px;">'
                    f'{indent}↳ <a href="{reverse("admin:titles_series_change", args=[sub.pk])}">'
                    f'{sub.title}</a>'
                    f'{" (#" + str(sub.series_parent_position) + ")" if sub.series_parent_position else ""}'
                    f'</div>'
                )
                result.extend(render_subseries(sub, level + 1))
            return result

        subseries_html = render_subseries(obj)
        if not subseries_html:
            return _("No subseries")

        return format_html(
            '<div style="margin-left: -20px;">{}</div>',
            mark_safe("".join(subseries_html)),
        )

    subseries_list.short_description = _("Subseries")
