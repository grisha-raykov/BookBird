from django.urls import path

from . import views

app_name = "lists"

urlpatterns = [
    path(
        "",
        views.ReadingListView.as_view(),
        name="my_lists",
    ),
    path(
        "create/",
        views.ReadingListCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/",
        views.ReadingListDetailView.as_view(),
        name="list_detail",
    ),
    path(
        "add/<int:publication_id>/",
        views.AddToListView.as_view(),
        name="add_to_list",
    ),
    path(
        "remove/<int:publication_id>/<int:list_id>/",
        views.RemoveFromListView.as_view(),
        name="remove_from_list",
    ),
    path(
        "my-books/",
        views.MyBooksView.as_view(),
        name="my_books",
    ),
    path(
        "<int:pk>/delete/",
        views.ReadingListDeleteView.as_view(),
        name="delete",
    ),
    path(
        "move/<int:publication_id>/",
        views.MoveToListView.as_view(),
        name="move_to_list",
    ),
    path("<int:pk>/copy/", views.CopyListView.as_view(), name="copy"),
]
