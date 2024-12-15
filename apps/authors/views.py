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
        return (
            Author.objects.select_related("language")  # Optimize language lookups
            .only(
                "canonical_name", "language", "views", "image_url"
            )  # Fetch only needed fields
            .order_by(*self.ordering)
        )

    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Authors")
        return context


class AuthorDetailView(DetailView):
    """Display author details"""

    model = Author
    template_name = "authors/author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.canonical_name
        return context
