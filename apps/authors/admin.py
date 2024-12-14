from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "canonical_name",
        "last_name",
        "language",
        "birthdate",
        "deathdate",
        "views",
    ]
    ordering = ["-views"]
    search_fields = ["canonical_name", "legal_name", "last_name"]

    list_filter = ["language"]

    readonly_fields = [
        "id",
        "last_name",  # Auto-generated from canonical_name
        "birthdate",  # Auto-generated from components
        "deathdate",  # Auto-generated from components
        "views",
        "annual_views",
        "popularity_score",
    ]

    fieldsets = [
        (None, {"fields": ("canonical_name", "legal_name", "last_name", "language")}),
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
        (_("Online Presence"), {"fields": ("wikipedia_url", "image")}),
        (_("Statistics"), {"fields": ("views", "annual_views", "popularity_score")}),
        (_("Notes"), {"fields": ("notes",)}),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return self.readonly_fields
        # For new objects, allow editing views/stats
        return ["id", "last_name", "birthdate_display", "deathdate_display"]
