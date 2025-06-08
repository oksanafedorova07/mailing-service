from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = "Отправляет все активные рассылки"

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            status="Создана", start_time__lte=now, end_time__gte=now
        )

        for mailing in mailings:
            self.stdout.write(f"📨 Отправляем рассылку #{mailing.pk}")
            success_count = 0

            for client in mailing.clients.all():
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
                    mailing=mailing, status=status, server_response=response
                )

            mailing.status = "Запущена"
            mailing.save()

            self.stdout.write(
                f"✅ Рассылка #{mailing.pk} отправлена ({success_count}/{mailing.clients.count()})"
            )
