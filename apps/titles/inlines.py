from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.titles.models import (
    Title,
    TitleTransliteration,
    AuthorTitle,
    SeriesTransliteration,
)


class TitleTransliterationInline(admin.TabularInline):
    model = TitleTransliteration
    extra = 1
    min_num = 0


class VariantTitleInline(admin.TabularInline):
    model = Title
    fk_name = "parent_title"
    fields = ["title", "type", "language", "first_pub_date"]
    readonly_fields = ["type", "language", "first_pub_date"]
    extra = 0
    show_change_link = True
    verbose_name = _("Variant Title")
    verbose_name_plural = _("Variant Titles")
    can_delete = False

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("language")
            .only(
                "title", "type", "language__name", "first_pub_date", "parent_title_id"
            )
        )


class SeriesTitleInline(admin.TabularInline):
    model = Title
    fk_name = "series"
    fields = ["title", "series_position", "type", "language"]
    readonly_fields = ["type", "language"]
    extra = 0
    can_delete = False
    show_change_link = True
    verbose_name = _("Title")
    verbose_name_plural = _("Titles in Series")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("language")
            .only(
                "title",
                "series_position",
                "type",
                "language__name",
            )
            .order_by("series_position")
        )


class AuthorTitleInline(admin.TabularInline):
    model = AuthorTitle
    extra = 1
    autocomplete_fields = ["author"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("author")
            .order_by("role", "author__last_name")
        )


class SeriesTransliterationInline(admin.TabularInline):
    model = SeriesTransliteration
    extra = 1
    min_num = 0
