from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from events.models import Event
from events.forms import AddCartForm
from accounts.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PaymentMethodForm, DiscountForm
from .models import CartModel
from .models import DiscountCode
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Create your views here.

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        form = DiscountForm()
        return render(request, 'cart/cart_view.html', {'cart': cart, 'form': form})


class CreatOrderView(View):
    def get(self, request):
        cart = Cart(request)
        tickets = cart.save_tickets()
        orders = cart.save_cart(tickets)
        print(orders.id)
        return redirect('cart:confirm_cart', orders.id)


class AddCartView(LoginRequiredMixin, View):
    def post(self, request, ev_id):
        cart = Cart(request)
        event = get_object_or_404(Event, id=ev_id)
        form = AddCartForm(request.POST)

        if form.is_valid():
            cart.add(event, form.cleaned_data['quantity'])
            return redirect('cart:cart_view')


class RemoveCartView(View):
    def post(self, request, ev_id):
        cart = Cart(request)
        event = get_object_or_404(Event, id=ev_id)
        cart.remove(event)
        return redirect('cart:cart_view')


class ConfirmCartView(View):
    def get(self, request, ord_id):
        user = request.user
        order = get_object_or_404(CartModel, id=ord_id)
        form1 = UserUpdateForm(instance=user)
        form2 = PaymentMethodForm()
        return render(request, 'cart/final_view.html', {'form1': form1,
                                                        'form2': form2,
                                                        'order': order,
                                                        })

    def post(self, request, ord_id):
        user = request.user
        order = get_object_or_404(CartModel, id=ord_id)
        cart = Cart(request)
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = PaymentMethodForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            pay_method = form2.cleaned_data['payment_methods']
            total_price = order.total_price

            payment_response = self.send_payment(request)

            if payment_response:
                cart.save_payment_info(pay_method, total_price, status='success')
                order.paid = True
                for ticket in order.tickets.all():
                    ticket.paid = True
                order.change_event_quantity()
                cart.clear()
                messages.success(request, 'Your payment was successful!', 'success')
                return redirect('home:home')
            else:
                cart.save_payment_info(pay_method, total_price, status='error')
                messages.warning(request, 'Your payment has error!', 'warning')
                return render(request, 'cart/final_view.html', {'form1': form1,
                                                                'form2': form2,
                                                                'cart': cart})

        return render(request, 'cart/final_view.html', {'form1': form1,
                                                        'form2': form2,
                                                        'cart': cart})

    def send_payment(self, request):
        """uncomplete"""
        return True



# class ApplyDiscountView(View):
#     def post(self, request):
#         form = DiscountForm(request.POST)
#         cart = Cart(request)
#         total = cart.get_total_price()
#
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             try:
#                 discount = DiscountCode.objects.get(code__exact=code)
#                 if discount.is_valid():
#
#
#             except DiscountCode.DoesNotExist:
#                 pass



