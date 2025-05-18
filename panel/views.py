from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from events.models import Event
from cart.models import CartModel, Ticket, Payment, DiscountCode
from accounts.models import User
from accounts.forms import UserUpdateForm


# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'panel/index.html')


class EventsView(ListView):
    model = Event
    template_name = 'panel/events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


class TicketsView(ListView):
    model = Ticket
    template_name = 'panel/tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class PaymentsView(ListView):
    model = Payment
    template_name = 'panel/payment.html'
    context_object_name = 'payments'

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        for item in Payment.objects.filter(from_user=self.request.user.id):
            print(item)
        return Payment.objects.filter(from_user=self.request.user.id)


class OrdersView(ListView):
    model = CartModel
    template_name = 'panel/orders.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return CartModel.objects.filter(user=self.request.user)


class DiscountsView(ListView):
    model = DiscountCode
    template_name = 'panel/discounts.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        return DiscountCode.objects.filter(user=self.request.user)


class AlterAccountView(View):
    form_class = UserUpdateForm
    template_name = 'panel/update.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            existing_user = User.objects.filter(
                phone_number=form.cleaned_data['phone_number']
            ).exclude(pk=request.user.pk).first()

            if existing_user:
                form.add_error('phone_number', 'This phone number is already in use.')
                return render(request, self.template_name, {'form': form})

            form.save()
            return redirect('panel:index')
        return render(request, self.template_name, {'form': form})
