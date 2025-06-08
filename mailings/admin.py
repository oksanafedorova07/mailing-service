from django.contrib import admin

from .models import Mailing, MailingAttempt, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status")
    list_filter = ("status",)
    filter_horizontal = ("clients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing", "time", "status", "server_response")
    list_filter = ("status", "mailing")
