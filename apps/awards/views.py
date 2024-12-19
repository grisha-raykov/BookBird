# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Award, AwardType


class AwardListView(ListView):
    model = AwardType
    template_name = "awards/award_list.html"
    context_object_name = "award_types"

    def get_queryset(self):
        return AwardType.objects.prefetch_related("categories", "awards").order_by(
            "name"
        )


class AwardTypeDetailView(DetailView):
    model = AwardType
    template_name = "awards/award_type_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters
        year = self.request.GET.get("year")
        category = self.request.GET.get("category")

        # Base queryset
        awards_qs = Award.objects.filter(type=self.object)

        # Apply filters
        if year:
            awards_qs = awards_qs.filter(year=year)
        if category:
            awards_qs = awards_qs.filter(category_id=category)

        # Get all available years for filtering
        years = (
            Award.objects.filter(type=self.object)
            .values_list("year", flat=True)
            .distinct()
            .order_by("-year")
        )

        context.update(
            {
                "categories": self.object.categories.all(),
                "awards": (
                    awards_qs.select_related("category")
                    .prefetch_related("title_awards__title")
                    .order_by("-year", "category__name", "level")
                ),
                "years": years,
                "selected_year": year,
                "selected_category": int(category) if category else None,
            }
        )
        return context


class AwardDetailView(DetailView):
    model = Award
    template_name = "awards/award_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titles"] = self.object.title_awards.select_related("title").all()
        return context
