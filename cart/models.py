from django.db import models
from events.models import Event
from accounts.models import User


# Create your models here.


class Payment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
