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
    """Display author details"""

    model = Author
    template_name = "authors/author_detail.html"
    context_object_name = "author"

    def get_queryset(self):
        return Author.objects.select_related("language").prefetch_related(
            "titles__series", "titles__language"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.canonical_name

        # Group titles by series
        titles = self.object.titles.all()
        series_titles = {}
        standalone_titles = []

        for title in titles:
            if title.series:
                if title.series not in series_titles:
                    series_titles[title.series] = []
                series_titles[title.series].append(title)
            else:
                standalone_titles.append(title)

        context["series_titles"] = series_titles
        context["standalone_titles"] = standalone_titles
        return context
