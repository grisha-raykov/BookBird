from django.db.models import Q, F, Prefetch
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView

from apps.publications.models import Publication, PublicationTitle
from ..titles.models import AuthorTitle


# Create your views here.
class PublicationListView(ListView):
    model = Publication
    template_name = "publications/publication_list.html"
    context_object_name = "publications"
    paginate_by = 25

    def get_queryset(self):
        """Get publications ordered by their titles' annual views"""
        queryset = (
            Publication.objects.select_related(
                "publisher",
            )
            .prefetch_related(
                "contained_titles__title",
            )
            .annotate(
                title_annual_views=F("contained_titles__title__annual_views"),
            )
            .order_by(
                "-title_annual_views",
                "title",
                "-publication_date",
            )
            .only(
                "title",
                "publication_date",
                "publisher__name",
                "format",
                "image_url",
            )
        )

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(isbn__icontains=query)
                | Q(publisher__name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Publications")
        if self.request.GET.get("q"):
            context["search_query"] = self.request.GET["q"]
        return context


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "publications/publication_detail.html"
    context_object_name = "publication"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Publication Details")
        return context

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("publisher", "publication_series")
            .prefetch_related(
                Prefetch(
                    "contained_titles",
                    queryset=PublicationTitle.objects.select_related(
                        "title", "title__series"
                    ).prefetch_related(
                        Prefetch(
                            "title__author_relationships",
                            queryset=AuthorTitle.objects.select_related("author"),
                        )
                    ),
                )
            )
        )
