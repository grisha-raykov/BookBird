from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "rating", "created_at", "updated_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["title__title", "user__username", "text"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        (None, {"fields": ("user", "title", "rating", "text")}),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "title")
