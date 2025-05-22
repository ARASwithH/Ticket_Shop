from django.db import models
from django.utils.text import slugify
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    image = models.ImageField(upload_to='events/%Y/%m/%d/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rated = models.BooleanField(default=False)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='events', blank=True)

    def __str__(self):
        return self.name

    def update_rate(self):
        from django.db.models import Avg
        result = self.event_rates.aggregate(avg=Avg('value'))
        self.rate = round(result['avg'], 1) if result['avg'] else None
        self.save()

class Rate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_rates')
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rates')

