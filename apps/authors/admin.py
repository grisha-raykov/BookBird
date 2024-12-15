from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import AuthorAdminForm
from .models import Author, AuthorTransliteration


class AuthorTransliterationInline(admin.TabularInline):
    model = AuthorTransliteration
    extra = 1
    min_num = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
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
        "views",  # Make views read-only
        "annual_views",  # Make annual_views read-only
        "popularity_score",  # Make popularity_score read-only
        "display_image",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "canonical_name",
                    "legal_name",
                    "last_name",
                    ("transliterated_canonical_name", "transliterated_legal_name"),
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
            {"fields": ("notes", "isfdb_id")},
        ),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return self.readonly_fields
        return [
            "id",
            "last_name",
            "views",
            "annual_views",
            "popularity_score",
        ]  # only these readonly for new objects

    def display_image(self, obj):
        """Display author image if url is provided"""
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.image_url,
            )
        return _("No image available")

    display_image.short_description = _("Image")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Handle canonical name transliteration
        if form.cleaned_data.get("transliterated_canonical_name"):
            AuthorTransliteration.objects.update_or_create(
                author=obj,
                type="CANONICAL",
                defaults={
                    "transliterated_name": form.cleaned_data[
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
                    "transliterated_name": form.cleaned_data[
                        "transliterated_legal_name"
                    ]
                },
            )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return self.readonly_fields
        return ["id", "last_name", "views", "annual_views", "popularity_score"]
