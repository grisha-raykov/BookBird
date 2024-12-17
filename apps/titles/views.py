from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Title
from ..publications.models import PublicationTitle


class TitleListView(ListView):
    """Display paginated list of titles"""

    model = Title
    template_name = "titles/title_list.html"
    context_object_name = "titles"
    paginate_by = 25
    ordering = ["-views", "title"]

    def get_queryset(self):
        return (
            Title.objects.select_related("language")
            .only("title", "language", "views", "first_pub_date", "type")
            .order_by(*self.ordering)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Books")
        return context


class TitleDetailView(DetailView):
    model = Title
    template_name = "titles/title_detail.html"
    context_object_name = "title"

    def get_queryset(self):
        return Title.objects.select_related(
            "language",
            "series",
            "series__parent",
            "parent_title",
        ).prefetch_related(
            "authors",
            "variant_titles",
            Prefetch(
                "publication_appearances",
                queryset=PublicationTitle.objects.select_related(
                    "publication",
                    "publication__publisher",
                ).order_by("publication__publication_date"),
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publication_cover"] = (
            self.object.publication_appearances.exclude(
                publication__image_url__isnull=True
            )
            .exclude(publication__image_url="")
            .first()
        )
        return context
