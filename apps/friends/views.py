from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from .models import Friendship
from apps.lists.models import ReadingList, ListItem


class FriendListView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = "friends/friend_list.html"
    context_object_name = "friendships"

    def get_queryset(self):
        return Friendship.objects.filter(
            user=self.request.user, status=Friendship.ACCEPTED
        ).select_related("friend")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_requests_count"] = Friendship.objects.filter(
            friend=self.request.user, status=Friendship.PENDING
        ).count()
        context["requests"] = Friendship.objects.filter(
            friend=self.request.user, status=Friendship.PENDING
        ).select_related("user")
        return context


class FriendRequestsView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = "friends/friend_requests.html"
    context_object_name = "requests"

    def get_queryset(self):
        return Friendship.objects.filter(
            friend=self.request.user, status=Friendship.PENDING
        ).select_related("user")


class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        friend = get_object_or_404(User, id=user_id)
        if friend != request.user:
            Friendship.objects.get_or_create(
                user=request.user,
                friend=friend,
                defaults={"status": Friendship.PENDING},
            )
        return JsonResponse({"success": True})


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, friendship_id):
        friendship = get_object_or_404(
            Friendship, id=friendship_id, friend=request.user, status=Friendship.PENDING
        )

        friendship.status = Friendship.ACCEPTED
        friendship.save()

        Friendship.objects.update_or_create(
            user=request.user,
            friend=friendship.user,
            defaults={"status": Friendship.ACCEPTED},
        )

        return JsonResponse({"success": True})


class FriendListsView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = "friends/friend_lists.html"
    context_object_name = "reading_lists"

    def get_queryset(self):
        friend = get_object_or_404(User, id=self.kwargs["friend_id"])
        return ReadingList.objects.filter(user=friend)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friend"] = get_object_or_404(User, id=self.kwargs["friend_id"])
        return context


class CopyListView(LoginRequiredMixin, View):
    def post(self, request, list_id):
        source_list = get_object_or_404(ReadingList, id=list_id)

        new_list = ReadingList.objects.create(
            user=request.user, name=f"Copy of {source_list.name}", list_type="custom"
        )

        for item in source_list.items.all():
            ListItem.objects.create(reading_list=new_list, publication=item.publication)

        return JsonResponse({"success": True, "message": _("List copied successfully")})


class UserSearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "")
        if len(query) >= 3:
            users = (
                User.objects.filter(username__icontains=query)
                .exclude(id=request.user.id)
                .exclude(
                    friend_requests__user=request.user,
                    friend_requests__status=Friendship.ACCEPTED,
                )[:10]
            )

            return JsonResponse(
                {
                    "users": [
                        {"id": user.id, "username": user.username} for user in users
                    ]
                }
            )
        return JsonResponse({"users": []})


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, friendship_id):
        friendship = get_object_or_404(Friendship, id=friendship_id, user=request.user)
        friendship.delete()
        return JsonResponse({"success": True})
