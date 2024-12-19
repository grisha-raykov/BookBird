from django.contrib import admin

from apps.lists.models import ReadingList, ListItem


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "list_type", "is_default", "created_at"]
    list_filter = ["list_type", "is_default"]
    search_fields = ["name", "user__username"]
    readonly_fields = ["is_default"]


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ["reading_list", "publication", "added_at"]
    list_filter = ["reading_list__list_type"]
    search_fields = ["reading_list__name", "publication__title"]
