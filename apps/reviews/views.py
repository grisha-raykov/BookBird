from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from django.utils.translation import gettext as _
from .forms import ReviewForm
from .models import Review
from ..titles.models import Title


class EditReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy("titles:detail", kwargs={"pk": self.object.title.pk})


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy("titles:detail", kwargs={"pk": self.object.title.pk})


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(Title, pk=self.kwargs["title_id"])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        try:
            return super().form_valid(form)
        except IntegrityError:
            # Handle unique constraint violation
            form.add_error(None, _("You have already reviewed this title"))
            return self.form_invalid(form)

    def form_invalid(self, form):
        title_id = self.kwargs["title_id"]
        # Store form data and errors in session
        self.request.session["form_errors"] = form.errors
        self.request.session["form_data"] = form.data
        # Redirect back to title detail page
        return redirect("titles:detail", pk=title_id)

    def get_success_url(self):
        return reverse_lazy("titles:detail", kwargs={"pk": self.kwargs["title_id"]})
