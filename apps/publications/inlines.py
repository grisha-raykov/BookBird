from django.contrib import admin

from apps.publications.models import PublicationAuthor, PublicationTitle


class PublicationAuthorInline(admin.TabularInline):
    model = PublicationAuthor
    extra = 0


class PublicationTitleInline(admin.TabularInline):
    model = PublicationTitle
    extra = 0
    readonly_fields = ["isfdb_id", "title", "page"]
