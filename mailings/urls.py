from django.urls import path

from .views import (MailingAttemptListView, MailingCreateView,
                    MailingDeleteView, MailingDetailView, MailingListView,
                    MailingSendView, MailingUpdateView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageListView,
                    MessageUpdateView, home_view)

app_name = "mailings"

urlpatterns = [
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailings/<int:pk>/update/",
        MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailings/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path("", home_view, name="home"),
    path("attempts/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
]
