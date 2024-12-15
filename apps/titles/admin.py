from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .choices import TitleType
from .forms import TitleAdminForm
from .models import Title, TitleTransliteration, Series


class TitleTransliterationInline(admin.TabularInline):
    model = TitleTransliteration
    extra = 1
    min_num = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    forms = TitleAdminForm
    inlines = [TitleTransliterationInline]
    list_display = ["title", "type", "language", "is_canonical", "first_pub_date"]

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
        "title",  # Allow searching by title
        "language",
        "=id",  # Allow searching by exact ID
        "parent_title__title",  # Search in parent titles
    ]

    readonly_fields = [
        "id",
        "first_pub_year",
        "first_pub_month",
        "first_pub_day",
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
                )
            },
        ),
        (
            _("Publication Details"),
            {"fields": ("first_pub_date",)},
        ),
        (
            _("Title Relationships"),
            {
                "fields": (
                    "parent_title",
                    "is_canonical",
                )
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

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return self.readonly_fields
        return ["id"]  # only id readonly when creating new object

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Make story_length required for short fiction
        if obj and obj.type == TitleType.SHORTFICTION:
            form.base_fields["story_length"].required = True

        return form


class SubseriesInline(admin.TabularInline):
    """Inline admin for subseries"""

    model = Series
    fk_name = "parent"
    extra = 0
    fields = ["title", "series_parent_position", "series_note"]
    ordering = ["series_parent_position"]
    show_change_link = True


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "series_parent_position"]
    search_fields = ["title"]
    readonly_fields = ["isfdb_id"]
    # list_filter = ["parent"]

    inlines = [SubseriesInline]

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
                )
            },
        ),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Prevent circular references by excluding self and children
            form.base_fields["parent"].queryset = Series.objects.exclude(
                pk__in=[obj.pk] + list(obj.subseries.values_list("id", flat=True))
            )
        return form

    class Media:
        css = {"all": ["admin/css/series.css"]}  # Optional custom styling
