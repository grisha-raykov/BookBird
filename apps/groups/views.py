from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from .models import ReadingGroup, GroupDiscussion, GroupMembership, DiscussionComment
from .forms import (
    ReadingGroupForm,
    GroupDiscussionForm,
    DiscussionCommentForm,
)
from ..titles.models import Title


class GroupListView(LoginRequiredMixin, ListView):
    model = ReadingGroup
    template_name = "groups/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        queryset = ReadingGroup.objects.filter(
            members=self.request.user,
        ).distinct()

        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return (
            queryset.select_related("creator")
            .prefetch_related("members")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search")

        other_groups = ReadingGroup.objects.filter(is_private=False)
        if search_query:
            other_groups = other_groups.filter(name__icontains=search_query)

        context["search_query"] = search_query
        context["other_groups"] = (
            other_groups.exclude(members=self.request.user)
            .select_related("creator")
            .prefetch_related("members")
            .order_by("-created_at")[:6]
        )
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = ReadingGroup
    template_name = "groups/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discussion_form"] = GroupDiscussionForm()
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = ReadingGroup
    form_class = ReadingGroupForm
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("groups:list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response


class GroupDiscussionCreateView(LoginRequiredMixin, CreateView):
    model = GroupDiscussion
    form_class = GroupDiscussionForm
    template_name = "groups/discussion_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = get_object_or_404(ReadingGroup, pk=self.kwargs["group_id"])
        title_id = self.request.GET.get("title")
        if title_id:
            context["title"] = get_object_or_404(Title, pk=title_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill the title field if provided in query params
        title_id = self.request.GET.get("title")
        if title_id:
            initial["title"] = title_id
        return initial

    def form_valid(self, form):
        form.instance.started_by = self.request.user
        form.instance.group_id = self.kwargs["group_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("groups:detail", kwargs={"pk": self.kwargs["group_id"]})


class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReadingGroup
    form_class = ReadingGroupForm
    template_name = "groups/group_form.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user

    def get_success_url(self):
        return reverse_lazy("groups:detail", kwargs={"pk": self.object.pk})


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReadingGroup
    success_url = reverse_lazy("groups:list")

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user


class RemoveMemberView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        membership = get_object_or_404(GroupMembership, id=self.kwargs["membership_id"])
        return membership.group.creator == self.request.user

    def post(self, request, membership_id):
        membership = get_object_or_404(GroupMembership, id=membership_id)

        # Don't allow removing the creator
        if membership.user == membership.group.creator:
            return JsonResponse(
                {"success": False, "message": _("Cannot remove the group creator")},
                status=400,
            )

        membership.delete()
        return JsonResponse(
            {"success": True, "message": _("Member removed successfully")}
        )


class GroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ReadingGroup.objects.all()

        if not self.request.user.is_authenticated:
            return ReadingGroup.objects.none()

        qs = qs.filter(Q(is_private=False) | Q(members=self.request.user))

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs.select_related("creator").order_by("name")

    def get_results(self, context):
        return [
            {
                "id": group.pk,
                "text": f"{group.name} ({group.members.count()} members)",
            }
            for group in context["object_list"]
        ]


class JoinGroupView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(ReadingGroup, pk=pk)

        # Check if user is already a member
        if group.members.filter(id=request.user.id).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": _("You are already a member of this group"),
                },
                status=400,
            )

        # Add user as member
        GroupMembership.objects.create(
            user=request.user, group=group, role=GroupMembership.MEMBER
        )

        return JsonResponse(
            {"success": True, "message": _("Successfully joined the group")}
        )


class LeaveGroupView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(ReadingGroup, pk=pk)

        # Don't allow the creator to leave
        if group.creator == request.user:
            return JsonResponse(
                {
                    "success": False,
                    "message": _("Group creators cannot leave their own groups"),
                },
                status=400,
            )

        # Remove user from group
        membership = get_object_or_404(GroupMembership, user=request.user, group=group)
        membership.delete()

        return JsonResponse(
            {"success": True, "message": _("Successfully left the group")}
        )


class DiscussionDetailView(LoginRequiredMixin, DetailView):
    model = GroupDiscussion
    template_name = "groups/discussion_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = DiscussionCommentForm()
        context["group"] = self.object.group
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    model = DiscussionComment
    form_class = DiscussionCommentForm

    def form_valid(self, form):
        discussion = get_object_or_404(
            GroupDiscussion, pk=self.kwargs["pk"], group_id=self.kwargs["group_id"]
        )
        form.instance.discussion = discussion
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "groups:discussion_detail",
            kwargs={"group_id": self.kwargs["group_id"], "pk": self.kwargs["pk"]},
        )


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(DiscussionComment, pk=pk, user=request.user)
        comment.delete()
        return JsonResponse(
            {
                "success": True,
                "message": _("Comment deleted successfully"),
            }
        )
