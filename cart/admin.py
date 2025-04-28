from django.contrib import admin

from .cart import Cart
from .models import CartModel, Payment, Ticket

# Register your models here.

admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(CartModel)
