from django.contrib import admin

from apps.publications.inlines import PublicationTitleInline
from apps.publications.models import Publisher, Publication
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    readonly_fields = ["isfdb_id"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "publication_date",
        "publisher",
        "format",
        "isbn",
    ]
    list_filter = ["format", "ctype", "publisher"]
    search_fields = ["title", "isbn"]
    readonly_fields = ["isfdb_id"]
    inlines = [PublicationTitleInline]

    fieldsets = [
        (
            _("Basic Information"),
            {
                "fields": (
                    "title",
                    "publication_date",
                    "publisher",
                    "isbn",
                    "isfdb_id",

                ),
            },
        ),
        # (
        #     _("Publication Details"),
        #     {
        #         "fields": (
        #             "format",
        #             "ctype",
        #             "pages",
        #             "price",
        #             "catalog_id",
        #         )
        #     },
        # ),
        # (
        #     _("Series Information"),
        #     {
        #         "fields": (
        #             "publication_series",
        #             "series_number",
        #         )
        #     },
        # ),
        (
            _("Additional Information"),
            {
                "fields": (
                    "image_url",
                    "isfdb_tag",
                ),
                "classes": ("collapse",),
            },
        ),
    ]
