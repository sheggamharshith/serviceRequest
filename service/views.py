from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic.base import View

from .models import ServiceRequest


class HomePageView(LoginRequiredMixin, View):
    """
    View for the home page.

    Only staff and superusers can view this page.
    If the user is not a staff or superuser, they will be redirected to the service request list page.
    """

    def get(self, request):
        """
        Render the home page template if the user is a staff or superuser.
        Otherwise, redirects the user to the service request list page.
        """
        if request.user.is_staff or request.user.is_superuser:
            return render(request, "home.html")
        return redirect("service_request_list")


class LandingPageView(View):
    """View for the landing page."""

    def get(self, request):
        """Render the landing page template."""
        return render(request, "landing.html")


class ServiceView(ListView):
    """View for displaying the service requests for the current user."""

    model = ServiceRequest
    template_name = "ServiceRequest.html"

    def get_queryset(self):
        """Return the service requests for the current user."""
        return ServiceRequest.objects.filter(User=self.request.user)


class CreateServiceView(CreateView):
    """View for creating a new service request."""

    model = ServiceRequest
    template_name = "create_service_request.html"
    fields = ["title", "description", "repair_service"]
    success_url = reverse_lazy("service_request_list")

    def form_valid(self, form):
        """Set the user of the new service request to the current user."""
        form.instance.User = self.request.user
        return super().form_valid(form)


class DetailServiceView(DetailView):
    """View for displaying the details of a service request."""

    model = ServiceRequest
    template_name = "detail_service_request.html"


class DeleteServiceView(DeleteView):
    """View for deleting a service request."""

    model = ServiceRequest
    template_name = "delete.html"
    success_url = reverse_lazy("service_request_list")

    def form_valid(self, form):
        """Soft deletes the service request and redirects to the service request list page."""
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
