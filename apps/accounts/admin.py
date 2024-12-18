from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.utils.translation import gettext_lazy as _


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _("Profile")
    fk_name = "user"


# @admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        # No inline on the user inline page
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
