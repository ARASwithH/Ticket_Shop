from django.db import models
from events.models import Event
from accounts.models import User
from django.utils import timezone
import string
import random


# Create your models here.

def generate_unique_code(length=10):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not DiscountCode.objects.filter(code=code).exists():
            return code


class Payment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')

    def __str__(self):
        return f'{str(self.from_user)} - {self.amount}'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    quantity = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)

    def get_total_price(self):
        return int(self.quantity) * int(self.event.price_per_ticket)

    def __str__(self):
        return f'{self.user} - {self.event} - {self.quantity}'


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    tickets = models.ManyToManyField(Ticket)
    total_price = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.tickets}'

    def change_event_quantity(self):
        for ticket in self.tickets.all():
            ticket.event.capacity -= ticket.quantity
            ticket.event.save()

        # event_ids = self.cart.keys()
        # events = Event.objects.filter(id__in=event_ids)
        #
        # for item in events:
        #     print(self.cart[f'{item.id}']['quantity'])
        #     print(item.capacity)
        #
        #     new_cap = item.capacity - int(self.cart[f'{item.id}']['quantity'])
        #     item.capacity = new_cap
        #     item.save()


class DiscountCode(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='discount_codes')
    discount_percent = models.PositiveIntegerField(help_text="e.g., 10 for 10%")
    active = models.BooleanField(default=True)
    valid_until = models.DateTimeField()

    def is_valid(self):
        return self.active and timezone.now() < self.valid_until

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} - {self.event}'


