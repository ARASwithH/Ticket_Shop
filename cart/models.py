from django.db import models
from events.models import Event
from accounts.models import User


# Create your models here.


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

    def __str__(self):
        return f'{self.user} - {self.event} - {self.quantity}'


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return f'{self.user} - {self.tickets}'
