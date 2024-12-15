from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from apps.authors.models import Author
from apps.titles.models import Title


class IndexView(TemplateView):
    """Home page of the application"""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": _("Welcome to BookBird"),
                "author_count": Author.objects.count(),
                "title_count": Title.objects.count(),
                "popular_authors": Author.objects.order_by("-views")[:6],
                "recent_titles": Title.objects.filter(is_canonical=True).order_by(
                    "-first_pub_date"
                )[:6],
            }
        )
        return context
