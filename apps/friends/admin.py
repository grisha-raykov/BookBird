from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["user", "friend", "status", "created_at", "updated_at"]
    list_filter = ["status"]
    search_fields = ["user__username", "friend__username"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        (
            None,
            {
                "fields": ("user", "friend", "status"),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "friend")
