from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from apps.authors.models import AuthorTransliteration, AuthorPseudonym
from apps.titles.models import AuthorTitle


class AuthorTransliterationInline(admin.TabularInline):
    model = AuthorTransliteration
    extra = 0
    min_num = 0

    def get_queryset(self, request):
        """Optimize inline queryset"""
        return (
            super()
            .get_queryset(request)
            .select_related("author")
            .only("type", "transliterated_text", "author_id")
            .order_by("type")
        )


class AuthorPseudonymInline(admin.TabularInline):
    model = AuthorPseudonym
    fk_name = "real_name"
    extra = 0
    readonly_fields = ["pseudonym_display"]
    fields = ["pseudonym_display"]
    can_delete = False
    show_change_link = True

    def pseudonym_display(self, obj):
        if obj.pseudonym:
            return obj.pseudonym.canonical_name
        return "-"

    pseudonym_display.short_description = _("Pseudonym")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("pseudonym")
            .only("pseudonym__canonical_name", "pseudonym__last_name")
            .order_by("pseudonym__last_name")
        )

    def has_add_permission(self, request, obj=None):
        return False


class AuthorTitleInline(admin.TabularInline):
    model = AuthorTitle
    extra = 0
    can_delete = False
    fields = ["title_link", "role"]
    readonly_fields = ["title_link", "role"]
    show_change_link = False

    def title_link(self, obj):
        url = reverse("admin:titles_title_change", args=[obj.title.id])
        return format_html('<a href="{}">{}</a>', url, obj.title.title)

    title_link.short_description = _("Title")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("title")
            .only("title__title", "title__id", "role")
            .order_by("title__title")
        )

    def has_add_permission(self, request, obj=None):
        return False
