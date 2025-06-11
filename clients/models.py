from django.conf import settings
from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

    owner = models.ForeignKey(  # ← связь с пользователем
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
    )

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        ordering = ['full_name']
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        constraints = [
            # Обеспечиваем уникальность email в рамках одного владельца
            models.UniqueConstraint(
                fields=['owner', 'email'],
                name='unique_owner_client_email'
            )
        ]
