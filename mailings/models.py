from django.conf import settings
from django.db import models

from clients.models import Client


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        default=1,  # временно, если есть миграции с существующими данными
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["-id"]  # Сортировка по ID (новые сверху)
        constraints = [
            # Уникальность темы сообщения для каждого пользователя
            models.UniqueConstraint(
                fields=["owner", "subject"],
                name="unique_owner_message_subject"
            )
        ]

class Mailing(models.Model):
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
    )

    def __str__(self):
        return f"Рассылка {self.pk} ({self.status})"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["-start_time"]  # Сортировка по дате начала (новые сверху)
        permissions = [
            ("can_change_status", "Может изменять статус рассылки"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="attempts"
    )

    def __str__(self):
        return f"Попытка {self.mailing_id} - {self.status}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-time"]  # Сортировка по времени попытки (новые сверху)
        indexes = [
            # Индекс для ускорения фильтрации по статусу
            models.Index(fields=["status"]),
            # Составной индекс для ускорения выборки по рассылке и времени
            models.Index(fields=["mailing", "time"]),
        ]
