from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.titles.models import Title


class ReadingGroup(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_groups",
        verbose_name=_("Creator"),
    )
    members = models.ManyToManyField(
        User,
        through="GroupMembership",
        related_name="reading_groups",
        verbose_name=_("Members"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    is_private = models.BooleanField(
        default=False,
    )
    image = models.URLField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Reading Group")
        verbose_name_plural = _("Reading Groups")

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (MEMBER, _("Member")),
        (MODERATOR, _("Moderator")),
        (ADMIN, _("Admin")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "group"]


class GroupDiscussion(models.Model):
    group = models.ForeignKey(
        ReadingGroup,
        on_delete=models.CASCADE,
        related_name="discussions",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="group_discussions",
    )
    topic = models.CharField(
        max_length=200,
        verbose_name=_("Topic"),
    )
    started_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="started_discussions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]


class DiscussionComment(models.Model):
    discussion = models.ForeignKey(
        GroupDiscussion,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
