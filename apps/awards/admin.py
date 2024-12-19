from django.contrib import admin

from .models import Award, AwardType, AwardCategory


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "year", "type", "category", "level"]
    list_filter = ["type", "category", "level", "year"]
    search_fields = ["title", "author"]
    readonly_fields = ["isfdb_id"]


@admin.register(AwardType)
class AwardTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "short_name", "is_poll", "is_non_genre"]
    search_fields = ["name", "code"]
    readonly_fields = ["isfdb_id"]


@admin.register(AwardCategory)
class AwardCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "order"]
    list_filter = ["type"]
    search_fields = ["name"]
    readonly_fields = ["isfdb_id"]
    ordering = ["type", "order"]
