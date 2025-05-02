from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta
from accounts import models
from django.utils import timezone


class Command(BaseCommand):
    help = "Delete all OTP_codes that expired"

    def handle(self, *args, **options):
        time_expired = timezone.now() - timedelta(minutes=2)
        models.OTPcode.objects.filter(created_at__lt=time_expired).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted OTP_codes'))
