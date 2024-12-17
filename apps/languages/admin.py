# Register your models here.
from django.contrib import admin
from .models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "native_name"]
    search_fields = ["name", "native_name", "code"]
    ordering = ["name"]
    readonly_fields = ["id"]

    fieldsets = [
        (None, {"fields": ("code", "name", "native_name")}),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + [
                "code",
                "name",
            ]
        return self.readonly_fields
