from django.db import models
from events.models import Event
from accounts.models import User
from django.utils import timezone
import string
import random
from collections import Counter


# Create your models here.

def generate_unique_code(length=10):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not DiscountCode.objects.filter(code=code).exists():
            return code

class DiscountCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, editable=False)
    event = models.ManyToManyField(Event, related_name='discount_codes')
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


class Payment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='0')

    def __str__(self):
        return f'{str(self.from_user)} - {self.amount}'

    @classmethod
    def get_total_amount(cls, user):
        all_payments = cls.objects.filter(from_user=user)
        total_expenses = 0
        for payment in all_payments:
            total_expenses += payment.amount

        return total_expenses

    @classmethod
    def get_most_common_payment_method(cls, user):
        all_payments = cls.objects.filter(from_user=user)
        method_counter = Counter()

        for payment in all_payments:
            method_counter.update([payment.payment_method])

        return method_counter.most_common(3)



class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    quantity = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)

    def get_total_price(self):
        return int(self.quantity) * int(self.event.price_per_ticket)

    def __str__(self):
        return f'{self.user} - {self.event} - {self.quantity}'

    @classmethod
    def get_most_common_categories(cls, user):
        all_tickets = cls.objects.filter(user=user)
        category_counter = Counter()

        for ticket in all_tickets:
            categories = ticket.event.get_categories()
            category_counter.update(cat.name for cat in categories)

        return category_counter.most_common(5)


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    tickets = models.ManyToManyField(Ticket)
    total_price = models.IntegerField()
    paid = models.BooleanField(default=False)
    discount = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.tickets}'

    def change_event_quantity(self):
        for ticket in self.tickets.all():
            ticket.event.capacity -= ticket.quantity
            ticket.event.save()

    def get_discounted_total_price(self):
        if self.discount is not None:
            return self.total_price * (100 - self.discount.discount_percent) / 100

    def get_total_price(self):
        return self.total_price

