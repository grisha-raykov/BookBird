from django.urls import path
from . import views

app_name = "awards"

urlpatterns = [
    path("", views.AwardListView.as_view(), name="list"),
    path("<int:pk>/", views.AwardDetailView.as_view(), name="detail"),
    path("type/<int:pk>/", views.AwardTypeDetailView.as_view(), name="type_detail"),
]
