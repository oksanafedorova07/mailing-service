from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from clients.models import Client
from mailings.models import Mailing, Message


class Command(BaseCommand):
    help = "Создаёт группу Менеджеры с нужными правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Менеджеры" создана'))
        else:
            self.stdout.write('⚠️ Группа "Менеджеры" уже существует')

        # Права только на просмотр
        models = [Mailing, Message, Client]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            view_permission = Permission.objects.get(
                codename=f"view_{model.__name__.lower()}",
                content_type=content_type,
            )
            group.permissions.add(view_permission)

        self.stdout.write(self.style.SUCCESS("🎉 Права добавлены"))
