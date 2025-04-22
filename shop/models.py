from django.db import models
from accounts.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name
