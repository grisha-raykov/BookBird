from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path(
        "",
        views.FriendListView.as_view(),
        name="list",
    ),
    path("search/", views.UserSearchView.as_view(), name="search"),
    path(
        "<int:friend_id>/lists/",
        views.FriendListsView.as_view(),
        name="lists",
    ),
    path(
        "requests/",
        views.FriendRequestsView.as_view(),
        name="requests",
    ),
    path(
        "add/<int:user_id>/",
        views.AddFriendView.as_view(),
        name="add",
    ),
    path(
        "accept/<int:friendship_id>/",
        views.AcceptFriendRequestView.as_view(),
        name="accept",
    ),
    path(
        "remove/<int:friendship_id>/",
        views.RemoveFriendView.as_view(),
        name="remove",
    ),
]
