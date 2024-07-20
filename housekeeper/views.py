from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import HousekeeperRequest
from django.contrib.auth.mixins import LoginRequiredMixin

class HousekeeperRequestListView(LoginRequiredMixin, ListView):
    model = HousekeeperRequest
    template_name = 'housekeeper_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return HousekeeperRequest.objects.filter(user=self.request.user)

class HousekeeperRequestCreateView(LoginRequiredMixin, CreateView):
    model = HousekeeperRequest
    template_name = 'housekeeper_request_form.html'
    fields = ['service_type', 'nationality']  # Add more fields as needed
    success_url = reverse_lazy('request-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HousekeeperRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = HousekeeperRequest
    template_name = 'housekeeper_request_form.html'
    fields = ['service_type', 'nationality']  # Add more fields as needed
    success_url = reverse_lazy('request-list')

class HousekeeperRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = HousekeeperRequest
    template_name = 'housekeeper_request_confirm_delete.html'
    success_url = reverse_lazy('request-list')
