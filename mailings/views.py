from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from clients.models import Client
from mailings.models import Mailing, MailingAttempt, Message


@cache_page(60 * 2)  # кеш на 2 минуты
def home_view(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="Запущена").count()
    unique_clients = Client.objects.values("email").distinct().count()

    return render(
        request,
        "mailings/home.html",
        {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_clients": unique_clients,
        },
    )


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingSendView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.owner != request.user:
            messages.error(request, "У вас нет прав на отправку этой рассылки.")
            return redirect("mailings:mailing_detail", pk=pk)

        clients = mailing.clients.all()
        success_count = 0

        for client in clients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                status = "Успешно"
                response = "OK"
                success_count += 1
            except Exception as e:
                status = "Не успешно"
                response = str(e)

            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=response,
            )

        mailing.status = "Запущена"
        mailing.save()

        messages.success(
            request,
            f"Рассылка отправлена. Успешно: {success_count}/{clients.count()}",
        )
        return redirect("mailings:mailing_detail", pk=pk)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailings/mailing_attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=user)
