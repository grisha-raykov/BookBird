from django.urls import path
from .views import PublicationListView

app_name = "publications"

urlpatterns = [
    path("", PublicationListView.as_view(), name="list"),
]
