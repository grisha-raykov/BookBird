from django.contrib import admin
from .models import ReadingGroup, GroupMembership, GroupDiscussion, DiscussionComment


@admin.register(ReadingGroup)
class ReadingGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "creator", "is_private", "created_at", "member_count"]
    list_filter = ["is_private", "created_at"]
    search_fields = ["name", "description", "creator__username"]

    def member_count(self, obj):
        return obj.members.count()

    member_count.short_description = "Members"


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "role", "joined_at"]
    list_filter = ["role", "joined_at"]
    search_fields = ["user__username", "group__name"]


@admin.register(GroupDiscussion)
class GroupDiscussionAdmin(admin.ModelAdmin):
    list_display = ["topic", "group", "started_by", "created_at", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["topic", "group__name", "started_by__username"]


@admin.register(DiscussionComment)
class DiscussionCommentAdmin(admin.ModelAdmin):
    list_display = ["discussion", "user", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["text", "user__username", "discussion__topic"]
