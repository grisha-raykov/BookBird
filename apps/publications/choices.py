from django.db import models
from django.utils.translation import gettext_lazy as _


class PublicationFormat(models.TextChoices):
    HC = "HC", _("Hardcover")
    TP = "TP", _("Trade Paperback")
    AUDIO_CASSETTE = "AUDIO_CASSETTE", _("Audio Cassette")
    PB = "PB", _("Paperback")
    QUARTO = "QUARTO", _("Quarto")
    UNKNOWN = "UNKNOWN", _("Unknown")
    PH = "PH", _("Pamphlet")
    DIGEST = "DIGEST", _("Digest")
    EBOOK = "EBOOK", _("Ebook")
    DOS = "DOS", _("Dos")
    PULP = "PULP", _("Pulp")
    DIGITAL_AUDIO_DOWNLOAD = "DIGITAL_AUDIO_DOWNLOAD", _("Digital Audio Download")
    AUDIO_MP3_CD = "AUDIO_MP3_CD", _("Audio MP3 CD")
    OTHER = "OTHER", _("Other")
    BEDSHEET = "BEDSHEET", _("Bedsheet")
    OCTAVO = "OCTAVO", _("Octavo")
    AUDIO_CD = "AUDIO_CD", _("Audio CD")
    WEBZINE = "WEBZINE", _("Webzine")
    A5 = "A5", _("A5")
    A4 = "A4", _("A4")
    AUDIO_LP = "AUDIO_LP", _("Audio LP")
    TABLOID = "TABLOID", _("Tabloid")
    DIGITAL_AUDIO_PLAYER = "DIGITAL_AUDIO_PLAYER", _("Digital Audio Player")


class PublicationType(models.TextChoices):
    ANTHOLOGY = "ANTHOLOGY", _("Anthology")
    CHAPBOOK = "CHAPBOOK", _("Chapbook")
    COLLECTION = "COLLECTION", _("Collection")
    MAGAZINE = "MAGAZINE", _("Magazine")
    NONFICTION = "NONFICTION", _("Non-Fiction")
    NOVEL = "NOVEL", _("Novel")
    OMNIBUS = "OMNIBUS", _("Omnibus")
    FANZINE = "FANZINE", _("Fanzine")
