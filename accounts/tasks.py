from celery import shared_task
from datetime import timedelta
from accounts import models
from django.utils import timezone

@shared_task
def remove_expired_otp_codes():
    time_expired = timezone.now() - timedelta(minutes=2)
    models.OTPcode.objects.filter(created_at__lt=time_expired).delete()