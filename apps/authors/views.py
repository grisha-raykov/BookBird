from django.db.models import Q, Prefetch
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Author
from ..awards.models import TitleAward, Award, AwardType


class AuthorListView(ListView):
    model = Author
    template_name = "authors/author_list.html"
    context_object_name = "authors"
    paginate_by = 25
    ordering = ["-views", "canonical_name"]

    def get_queryset(self):
        queryset = Author.objects.select_related("language").only(
            "canonical_name", "language", "views", "image_url"
        )

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(canonical_name__icontains=query)
                | Q(legal_name__icontains=query)
                | Q(last_name__icontains=query)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
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
        titles = self.object.titles.all().order_by("-views")[:100]
        award_wins = sum(
            title.awards.filter(award__level=1).count() for title in titles
        )
        award_nominations = sum(
            title.awards.filter(award__level=9).count() for title in titles
        )
        context.update(
            {"award_wins": award_wins, "award_nominations": award_nominations}
        )
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


class AuthorAwardsView(DetailView):
    model = Author
    template_name = "authors/author_awards.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all award types for this author
        award_types = (
            AwardType.objects.filter(
                awards__title_awards__title__in=self.object.titles.all()
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "awards",
                    queryset=Award.objects.filter(
                        title_awards__title__in=self.object.titles.all()
                    )
                    .select_related("category")
                    .prefetch_related(
                        Prefetch(
                            "title_awards",
                            queryset=TitleAward.objects.filter(
                                title__in=self.object.titles.all()
                            ).select_related("title"),
                        )
                    ),
                )
            )
        )
        context["award_types"] = award_types
        return context
