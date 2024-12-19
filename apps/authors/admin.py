from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .inlines import (
    AuthorTransliterationInline,
    AuthorPseudonymInline,
    AuthorTitleInline,
)
from .models import Author, AuthorTransliteration
from ..titles.models import AuthorTitle


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_form.html"
    # form = AuthorAdminForm
    inlines = [AuthorTransliterationInline, AuthorPseudonymInline, AuthorTitleInline]
    list_display = [
        "canonical_name",
        "last_name",
        "language",
        "birthdate",
        "deathdate",
        "views",
        "display_image",
    ]

    search_fields = [
        "canonical_name",
        "last_name",
        "legal_name",
    ]

    readonly_fields = [
        "id",
        "last_name",
        "birth_year",
        "birth_month",
        "birth_day",
        "death_year",
        "death_month",
        "death_day",
        "views",
        "annual_views",
        "popularity_score",
        "display_image",
        "isfdb_id",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "canonical_name",
                    "legal_name",
                    "last_name",
                    # ("transliterated_canonical_name", "transliterated_legal_name"),
                    "language",
                )
            },
        ),
        (
            _("Birth Information"),
            {
                "fields": (
                    "birthdate",
                    "birthplace",
                )
            },
        ),
        (
            _("Death Information"),
            {"fields": ("deathdate",)},
        ),
        (
            _("Online Presence"),
            {
                "fields": (
                    "wikipedia_url",
                    "imdb_url",
                    "image_url",
                    "display_image",
                )
            },
        ),
        (
            _("Statistics"),
            {
                "fields": (
                    "views",
                    "annual_views",
                    "popularity_score",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Additional Info"),
            {"fields": ("isfdb_id",)},
        ),
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("language")
            .prefetch_related(
                Prefetch(
                    "title_relationships",
                    queryset=(
                        AuthorTitle.objects.select_related(
                            "title", "title__language"
                        ).only(
                            "role",
                            "title__title",
                            "title__type",
                            "title__language__name",
                            "author_id",
                            "title_id",
                        )
                    ),
                ),
            )
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return [
            "id",
            "last_name",
            "views",
            "annual_views",
            "popularity_score",
        ]

    def display_image(self, obj):
        """Display author image if url is provided with fallback for failed loads"""
        if not obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png",
            )

        return format_html(
            """
            <img src="{}" 
                 style="max-height: 200px; max-width: 200px;"
                 onerror="this.onerror=null; this.src='{}'" />
        """,
            obj.image_url,
            "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png",
        )

    display_image.short_description = _("Image")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Handle canonical name transliteration
        if form.cleaned_data.get("transliterated_canonical_name"):
            AuthorTransliteration.objects.update_or_create(
                author=obj,
                type="CANONICAL",
                defaults={
                    "transliterated_text": form.cleaned_data[
                        "transliterated_canonical_name"
                    ]
                },
            )
        # Handle legal name transliteration
        if form.cleaned_data.get("transliterated_legal_name"):
            AuthorTransliteration.objects.update_or_create(
                author=obj,
                type="LEGAL",
                defaults={
                    "transliterated_text": form.cleaned_data[
                        "transliterated_legal_name"
                    ]
                },
            )
