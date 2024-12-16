from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.authors.models import AuthorTransliteration
from apps.titles.models import AuthorTitle


class AuthorTransliterationInline(admin.TabularInline):
    model = AuthorTransliteration
    extra = 1
    min_num = 0


class TitleAuthorInline(admin.TabularInline):
    model = AuthorTitle
    extra = 1
    autocomplete_fields = ["title"]
    fields = ["title", "role"]
    verbose_name = _("Title")
    verbose_name_plural = _("Titles")

    def get_queryset(self, request):
        """Optimize inline queryset"""
        return (
            super()
            .get_queryset(request)
            .select_related("title", "title__language")
            .order_by("title__title")
        )
