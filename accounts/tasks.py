from celery import shared_task
from datetime import timedelta

import utils
from accounts import models
from django.utils import timezone

from cart.models import Ticket
from events.models import Event

@shared_task
def remove_expired_otp_codes():
    time_expired = timezone.now() - timedelta(minutes=2)
    models.OTPcode.objects.filter(created_at__lt=time_expired).delete()


@shared_task
def event_ender():
    events = Event.objects.all()
    for event in events:
        if timezone.now() >= event.end_date:
            event.is_active = False
            event.save()


@shared_task
def event_ender_check():
    events = Event.objects.filter(is_active=False, rated=False)
    users_phone_number = {}

    if events.exists():
        for event in events:
            tickets = Ticket.objects.filter(event=event)

            if tickets.exists():
                for ticket in tickets:
                    if event.name not in users_phone_number:
                        users_phone_number[event.name] = []

                    users_phone_number[event.name].append(ticket.user.phone_number)

        if users_phone_number:
            utils.send_rating_sms(users_phone_number)

