from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Title


class TitleListView(ListView):
    """Display paginated list of titles"""

    model = Title
    template_name = "titles/title_list.html"
    context_object_name = "titles"
    paginate_by = 25
    ordering = ["-views", "title"]

    def get_queryset(self):
        """Get titles with optimized query"""
        return (
            Title.objects.select_related("language")
            # Remove is_canonical filter temporarily or update your data
            .only("title", "language", "views", "first_pub_date", "type")
            .order_by(*self.ordering)
        )

    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Books")
        return context


class TitleDetailView(DetailView):
    model = Title
    template_name = "titles/title_detail.html"
    context_object_name = "title"

    def get_queryset(self):
        return Title.objects.select_related("language").prefetch_related("authors")
