from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Author


class AuthorListView(ListView):
    """Display paginated list of authors"""

    model = Author
    template_name = "authors/author_list.html"
    context_object_name = "authors"
    paginate_by = 25
    ordering = ["-views", "canonical_name"]

    def get_queryset(self):
        """Get authors with optimized query"""
        """Get authors with optimized query"""
        queryset = Author.objects.select_related("language").only(
            "canonical_name", "language", "views", "image_url"
        )

        # Handle search
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(canonical_name__icontains=query)
                | Q(legal_name__icontains=query)
                | Q(last_name__icontains=query)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Authors")
        if self.request.GET.get("q"):
            context["search_query"] = self.request.GET["q"]
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = "authors/author_detail.html"
    context_object_name = "author"

    def get_queryset(self):
        return Author.objects.select_related("language")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.canonical_name
        titles = self.object.titles.all().order_by("-views")[:20]

        for title in titles:
            if not title.publication_appearances.filter(
                publication__image_url__isnull=False
            ).exists():
                next_oldest_publication = (
                    title.publication_appearances.filter(
                        publication__image_url__isnull=False
                    )
                    .order_by("publication__publication_date")
                    .first()
                )
                if next_oldest_publication:
                    title.publication_appearances = [next_oldest_publication]

        context["titles"] = titles
        return context
