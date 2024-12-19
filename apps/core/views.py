from django.db.models import Q, Prefetch
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.authors.models import Author
from apps.publications.models import Publication
from apps.titles.models import Title, Series, AuthorTitle


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adjusted popular titles query
        popular_titles = (
            Title.objects.select_related("series", "language")
            .prefetch_related(
                "publication_appearances",
                "publication_appearances__publication",
                Prefetch(
                    "author_relationships",
                    queryset=AuthorTitle.objects.select_related("author").order_by(
                        "author__canonical_name"
                    ),
                ),
            )
            .order_by("-annual_views", "-views")[:9]
        )

        context.update(
            {
                "title": _("Welcome to BookBird"),
                "author_count": Author.objects.count(),
                "title_count": Title.objects.count(),
                "popular_authors": Author.objects.order_by("-views")[:6],
                "popular_titles": popular_titles,
            }
        )
        return context


class GlobalSearchView(TemplateView):
    template_name = "search/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        context["query"] = query
        context["title"] = _("Search Results")

        if len(query) < 3:
            context["results"] = {}
            return context

        titles = (
            Title.objects.filter(
                Q(title__icontains=query) | Q(series__title__icontains=query)
            )
            .select_related("series", "language")
            .order_by("-annual_views", "-views", "title")
            .distinct()
        )

        # Search Authors - ordered by annual views
        authors = (
            Author.objects.filter(
                Q(canonical_name__icontains=query) | Q(legal_name__icontains=query)
            )
            .select_related("language")
            .order_by("-annual_views", "-views", "canonical_name")
        )

        series = (
            Series.objects.filter(title__icontains=query)
            .select_related("parent")
            .prefetch_related("titles")
            .annotate(
                total_annual_views=Sum("titles__annual_views"),
                total_views=Sum("titles__views"),
            )
            .order_by("-total_annual_views", "-total_views", "title")
            .distinct()
        )

        # Search Publications (ISBN)
        publications = Publication.objects.filter(
            Q(isbn__icontains=query.replace("-", ""))
        ).select_related("publisher")

        # Combine results
        context["results"] = {
            "titles": titles[:10],
            "authors": authors[:10],
            "series": series[:10],
            "publications": publications[:10],
        }

        return context
