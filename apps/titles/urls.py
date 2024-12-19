from django.urls import path
from .views import TitleListView, TitleDetailView, TitleAutocomplete, SeriesDetailView

app_name = "titles"

urlpatterns = [
    path("", TitleListView.as_view(), name="list"),
    path("<int:pk>/", TitleDetailView.as_view(), name="detail"),
    path(
        "ta",
        TitleAutocomplete.as_view(),
        name="ta",
    ),
    path("series/<int:pk>/", SeriesDetailView.as_view(), name="series_detail"),
]
