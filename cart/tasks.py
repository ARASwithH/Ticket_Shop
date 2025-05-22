from celery import shared_task
from datetime import timedelta
from accounts import models
from django.utils import timezone
from .models import Ticket
import utils


@shared_task
def ticket_reminder():
    tickets = Ticket.objects.all()
    for ticket in tickets:
        if ticket.event.start_date.day == timezone.now().day:
            utils.send_reminder(ticket)
