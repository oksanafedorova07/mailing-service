from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("clients:client_list")

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)
