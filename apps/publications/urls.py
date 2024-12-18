from django.urls import path
from .views import PublicationListView, PublicationDetailView

app_name = "publications"

urlpatterns = [
    path("", PublicationListView.as_view(), name="list"),
    path("<int:pk>/", PublicationDetailView.as_view(), name="detail"),
]
