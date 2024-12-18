from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext as _

from .models import ReadingList, ListItem
from .forms import ReadingListForm
from ..publications.models import Publication


class ReadingListView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = "lists/list_list.html"
    context_object_name = "reading_lists"

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


class ReadingListDetailView(LoginRequiredMixin, DetailView):
    model = ReadingList
    template_name = "lists/my_books.html"
    context_object_name = "selected_list"

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_items"] = (
            ListItem.objects.filter(reading_list=self.object)
            .select_related("publication", "reading_list")
            .order_by("-added_at")
        )
        return context


class ReadingListCreateView(LoginRequiredMixin, CreateView):
    model = ReadingList
    form_class = ReadingListForm
    template_name = "lists/list_form.html"
    success_url = reverse_lazy("lists:my_lists")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.list_type = "custom"
        return super().form_valid(form)


class AddToListView(LoginRequiredMixin, View):
    def post(self, request, publication_id):
        list_id = request.POST.get("list_id")
        if not list_id:
            return JsonResponse({"error": _("No list selected")}, status=400)

        reading_list = get_object_or_404(ReadingList, id=list_id, user=request.user)
        publication = get_object_or_404(Publication, id=publication_id)

        # Create or update list item
        ListItem.objects.get_or_create(
            reading_list=reading_list, publication=publication
        )

        return JsonResponse(
            {"success": True, "message": _("Added to list successfully")}
        )


class RemoveFromListView(LoginRequiredMixin, View):
    def post(self, request, publication_id, list_id):
        list_item = get_object_or_404(
            ListItem,
            reading_list__user=request.user,
            reading_list_id=list_id,
            publication_id=publication_id,
        )
        list_item.delete()
        return JsonResponse(
            {"success": True, "message": _("Removed from list successfully")}
        )


class MyBooksView(LoginRequiredMixin, ListView):
    model = ListItem
    template_name = "lists/my_books.html"
    context_object_name = "list_items"

    def get_queryset(self):
        return (
            ListItem.objects.filter(reading_list__user=self.request.user)
            .select_related("publication", "reading_list")
            .order_by("-added_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_list"] = None
        return context


class ReadingListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReadingList
    success_url = reverse_lazy("lists:my_lists")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user and not obj.is_default

    def delete(self, request, *args, **kwargs):
        if self.get_object().is_default:
            return JsonResponse(
                {"error": _("Default lists cannot be deleted")}, status=403
            )
        return super().delete(request, *args, **kwargs)


class MoveToListView(LoginRequiredMixin, View):
    def post(self, request, publication_id):
        list_id = request.POST.get("list_id")
        if not list_id:
            return JsonResponse({"error": _("No list selected")}, status=400)

        # Get the target list and publication
        new_list = get_object_or_404(ReadingList, id=list_id, user=request.user)
        publication = get_object_or_404(Publication, id=publication_id)

        # Remove from current list and add to new list
        ListItem.objects.filter(
            reading_list__user=request.user, publication=publication
        ).delete()

        ListItem.objects.create(reading_list=new_list, publication=publication)

        return JsonResponse(
            {
                "success": True,
                "message": _("Moved to list successfully"),
            }
        )


class CopyListView(LoginRequiredMixin, View):
    def post(self, request, pk):
        source_list = get_object_or_404(ReadingList, pk=pk)

        # Create new list
        new_list = ReadingList.objects.create(
            user=request.user, name=f"{source_list.name} (Copy)", list_type="custom"
        )

        # Copy all items
        items_to_create = [
            ListItem(reading_list=new_list, publication=item.publication)
            for item in source_list.items.all()
        ]
        ListItem.objects.bulk_create(items_to_create)

        return JsonResponse({"success": True, "message": _("List copied successfully")})
