from django.urls import path

from .views import (
    PublicationListView,
    PublicationDetailView,
    PublicationSeriesDetailView,
)

app_name = "publications"

urlpatterns = [
    path("", PublicationListView.as_view(), name="list"),
    path("<int:pk>/", PublicationDetailView.as_view(), name="detail"),
    path(
        "series/<int:pk>/", PublicationSeriesDetailView.as_view(), name="series_detail"
    ),
]
