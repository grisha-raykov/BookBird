from django.db import models
from django.utils.translation import gettext_lazy as _


class TitleType(models.TextChoices):
    ANTHOLOGY = "ANTHOLOGY", _("Anthology")
    BACKCOVERART = "BACKCOVERART", _("Back Cover Art")
    COLLECTION = "COLLECTION", _("Collection")
    COVERART = "COVERART", _("Cover Art")
    INTERIORART = "INTERIORART", _("Interior Art")
    EDITOR = "EDITOR", _("Editor")
    ESSAY = "ESSAY", _("Essay")
    INTERVIEW = "INTERVIEW", _("Interview")
    NOVEL = "NOVEL", _("Novel")
    NONFICTION = "NONFICTION", _("Non-Fiction")
    OMNIBUS = "OMNIBUS", _("Omnibus")
    POEM = "POEM", _("Poem")
    REVIEW = "REVIEW", _("Review")
    SERIAL = "SERIAL", _("Serial")
    SHORTFICTION = "SHORTFICTION", _("Short Fiction")
    CHAPBOOK = "CHAPBOOK", _("Chapbook")


class StoryLength(models.TextChoices):
    NOVELLA = "NOVELLA", _("Novella")
    NOVELETTE = "NOVELETTE", _("Novelette")
    SHORTSTORY = "SHORTSTORY", _("Short Story")


class AuthorRole(models.IntegerChoices):
    CANONICAL = 1, _("Canonical author entry")
    INTERVIEWEE = 2, _("Interviewee author")
    REVIEWEE = 3, _("Reviewee author")
