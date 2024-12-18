from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Title, AuthorTitle
from ..publications.models import PublicationTitle
from ..reviews.forms import ReviewForm


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
        """Add extra context"""
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
            Prefetch(
                "author_relationships",
                queryset=AuthorTitle.objects.select_related("author").order_by(
                    "role", "author__canonical_name"
                ),
            ),
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
        if self.request.session.get("form_errors"):
            form = ReviewForm(initial=self.request.session.get("form_data"))
            form._errors = self.request.session.pop("form_errors")
            context["form"] = form
            self.request.session.pop("form_data", None)
        else:
            context["form"] = ReviewForm()
        if self.request.user.is_authenticated:
            context["user_review"] = self.object.reviews.filter(
                user=self.request.user
            ).first()
            if not context["user_review"]:
                context["review_form"] = ReviewForm()

        context["reviews"] = self.object.reviews.select_related("user").order_by(
            "-created_at"
        )

        return context
