from django.core.management.base import BaseCommand
from cart.models import Ticket
from django.utils import timezone
import utils


class Command(BaseCommand):
    help = "send a reminder sms to user "

    def handle(self, *args, **options):
        tickets = Ticket.objects.all()
        for ticket in tickets:
            if ticket.event.start_date.day >= timezone.now().day:
                utils.send_reminder(ticket)

