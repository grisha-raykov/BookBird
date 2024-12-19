from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path(
        "",
        views.GroupListView.as_view(),
        name="list",
    ),
    path(
        "create/",
        views.GroupCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/",
        views.GroupDetailView.as_view(),
        name="detail",
    ),
    path("<int:pk>/edit/", views.GroupUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.GroupDeleteView.as_view(), name="delete"),
    path(
        "<int:group_id>/discussions/create/",
        views.GroupDiscussionCreateView.as_view(),
        name="discussion_create",
    ),
    path(
        "membership/<int:membership_id>/remove/",
        views.RemoveMemberView.as_view(),
        name="remove_member",
    ),
    path(
        "group-autocomplete/",
        views.GroupAutocomplete.as_view(),
        name="group-autocomplete",
    ),
    path(
        "<int:pk>/join/",
        views.JoinGroupView.as_view(),
        name="join",
    ),
    path(
        "<int:pk>/leave/",
        views.LeaveGroupView.as_view(),
        name="leave",
    ),
    path(
        "<int:group_id>/discussions/<int:pk>",
        views.DiscussionDetailView.as_view(),
        name="discussion_detail",
    ),
    path(
        "<int:group_id>/discussions/<int:pk>/comment/",
        views.AddCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "comments/<int:pk>/delete/",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
]
