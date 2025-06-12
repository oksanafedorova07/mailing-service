from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="customuser_set",  # Уникальное имя
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",  # Уникальное имя
        related_query_name="customuser",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta(AbstractUser.Meta):
        verbose_name = _("custom user")
        verbose_name_plural = _("custom users")
        ordering = ["-date_joined"]
        db_table = "custom_users"

        # Для совместимости с переопределёнными полями
        default_related_name = "custom_users"

        # Дополнительные индексы для оптимизации запросов
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["last_name", "first_name"], name="name_idx"),
        ]

        # Ограничения уникальности
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_user_email"),
            models.UniqueConstraint(fields=["username"], name="unique_username"),
        ]
