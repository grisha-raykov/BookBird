from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.authors.models import Author
from apps.titles.models import Title, Series
from apps.publications.models import Publication, Publisher
from apps.awards.models import Award


class Command(BaseCommand):
    help = "Create admin groups with different permission levels"

    def handle(self, *args, **kwargs):
        librarians, _ = Group.objects.get_or_create(name="Librarians")

        author_ct = ContentType.objects.get_for_model(Author)
        title_ct = ContentType.objects.get_for_model(Title)
        series_ct = ContentType.objects.get_for_model(Series)
        publication_ct = ContentType.objects.get_for_model(Publication)
        publisher_ct = ContentType.objects.get_for_model(Publisher)
        award_ct = ContentType.objects.get_for_model(Award)

        # Define limited permissions for Librarians
        librarian_perms = [
            # Author permissions
            Permission.objects.get(codename="view_author", content_type=author_ct),
            Permission.objects.get(codename="add_author", content_type=author_ct),
            Permission.objects.get(codename="change_author", content_type=author_ct),
            # Title permissions
            Permission.objects.get(codename="view_title", content_type=title_ct),
            Permission.objects.get(codename="add_title", content_type=title_ct),
            Permission.objects.get(codename="change_title", content_type=title_ct),
            # Series permissions
            Permission.objects.get(codename="view_series", content_type=series_ct),
            Permission.objects.get(codename="add_series", content_type=series_ct),
            Permission.objects.get(codename="change_series", content_type=series_ct),
        ]

        # Create Heads of Library group (full permissions)
        heads_of_library, _ = Group.objects.get_or_create(name="Heads of Library")

        # Define full permissions for Heads of Library
        head_librarian_perms = [
            # Full Author permissions
            *Permission.objects.filter(content_type=author_ct),
            # Full Title permissions
            *Permission.objects.filter(content_type=title_ct),
            # Full Series permissions
            *Permission.objects.filter(content_type=series_ct),
            # Full Publication permissions
            *Permission.objects.filter(content_type=publication_ct),
            # Full Publisher permissions
            *Permission.objects.filter(content_type=publisher_ct),
            # Full Award permissions
            *Permission.objects.filter(content_type=award_ct),
        ]

        librarians.permissions.set(librarian_perms)
        heads_of_library.permissions.set(head_librarian_perms)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created admin groups:\n"
                "- Librarians (limited CRUD)\n"
                "- Heads of Library (full CRUD)"
            )
        )
