from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView
)
from django.urls import reverse_lazy
from accounts.models import Role, Team, CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .models import Priority, Status, Issue


class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "body", "assignee", "status", "priority"]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def test_func(self):
        po_role = Role.objects.get(name="Product Owner")
        return self.request.user.role == po_role


class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "body", "assignee", "status", "priority"]

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user or issue.assignee == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user or issue.assignee == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_list = Status.objects.all()
        context["status_list"] = status_list
        return context

    def get_queryset(self):
        user = self.request.user
        if user.role.name == "Manager":
            queryset = super().get_queryset()
        else:
            user_team_name = self.request.user.team.name
            queryset = super().get_queryset().filter(assignee__team__name=user_team_name)
        return queryset


class ReportView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "issues/report.html"
    model = Issue
    context_object_name = "issue_list"

    def get_queryset(self):
        return super().get_queryset().order_by("-created_on")

    def test_func(self):
        po_role = Role.objects.get(name="Manager")
        return self.request.user.role == po_role

    def handle_no_permission(self):
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reporters"] = (
            CustomUser.objects.filter(reporter__status__name="Done")
            .annotate(issue_count=Count("reporter"))
            .values("username", "issue_count")
            .order_by("-issue_count")
        )
        return context
