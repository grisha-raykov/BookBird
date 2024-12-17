from django.urls import path
from .views import TitleListView, TitleDetailView

app_name = "titles"

urlpatterns = [
    path("", TitleListView.as_view(), name="list"),
    path("<int:pk>/", TitleDetailView.as_view(), name="detail"),
]
