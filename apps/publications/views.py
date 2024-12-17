from django.db.models import Q
from django.utils.translation import gettext as _
from django.views.generic import ListView

from apps.publications.models import Publication


# Create your views here.
class PublicationListView(ListView):
    model = Publication
    template_name = "publications/publication_list.html"
    context_object_name = "publications"

    paginate_by = 25
    ordering = ["-publication_date", "title"]

    def get_queryset(self):
        """Get publications with optimized query"""
        queryset = (
            Publication.objects.select_related("publisher")
            .only(
                "title",
                "publication_date",
                "publisher__name",
                "format",
                "ctype",
                "image_url",
            )
            .order_by(*self.ordering)
        )

        # Handle search
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
