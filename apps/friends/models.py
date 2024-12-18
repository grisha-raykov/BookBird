from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Friendship(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    STATUS_CHOICES = [
        (PENDING, _("Pending")),
        (ACCEPTED, _("Accepted")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships")
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_requests"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "friend"]
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendships")

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username} ({self.status})"
