from django.urls import path
from .views import AuthorListView, AuthorDetailView, AuthorAwardsView

app_name = "authors"

urlpatterns = [
    path(
        "",
        AuthorListView.as_view(),
        name="list",
    ),
    path(
        "<int:pk>/",
        AuthorDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/awards/",
        AuthorAwardsView.as_view(),
        name="awards",
    ),
]
