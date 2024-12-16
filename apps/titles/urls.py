from django.urls import path
from . import views

app_name = "titles"

urlpatterns = [
    path("", views.TitleListView.as_view(), name="list"),
    path("<int:pk>/", views.TitleDetailView.as_view(), name="detail"),
]
