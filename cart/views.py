from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from events.models import Event
from events.forms import AddCartForm
from accounts.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PaymentMethodForm, DiscountForm
from .models import CartModel, DiscountCode, Payment


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
        cart.clear()
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
        if order.discount is not None:
            discountform = DiscountForm(initial={'code': order.discount.code})
            discountform.fields['code'].widget.attrs['readonly'] = True
        else:
            discountform = DiscountForm()
        return render(request, 'cart/final_view.html', {'form1': form1,
                                                        'form2': form2,
                                                        'order': order,
                                                        'discountform': discountform,
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

            if order.discount is None:
                total_price = order.get_total_price()
            else:
                total_price = order.get_discounted_total_price()

            payment_response = self.send_payment(request)

            if payment_response:

                Payment.objects.create(
                    from_user=request.user,
                    amount=total_price,
                    payment_method=pay_method,
                    status='1'
                )

                order.paid = True
                order.save()

                for ticket in order.tickets.all():
                    ticket.paid = True
                    ticket.save()

                order.change_event_quantity()
                messages.success(request, 'Your payment was successful!', 'success')
                return redirect('home:home')
            else:
                Payment.objects.create(
                    from_user=request.user,
                    amount=total_price,
                    payment_method=pay_method,
                    status='0'
                )

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


class ApplyDiscountView(View):
    def get(self, request, ord_id):
        dc_code = request.GET.get('code')
        order = get_object_or_404(CartModel, id=ord_id)

        if not dc_code:
            messages.error(request, 'No discount code provided.', 'error')
            return redirect('cart:confirm_cart', ord_id)

        try:
            discount = DiscountCode.objects.get(code=dc_code)
        except DiscountCode.DoesNotExist:
            messages.error(request, 'Discount code does not exist!', 'error')
            return redirect('cart:confirm_cart', ord_id)

        if not discount.is_valid():
            messages.warning(request, 'Discount is expired or inactive!', 'warning')
            return redirect('cart:confirm_cart', ord_id)

        for ticket in order.tickets.all():
            if not discount.event.filter(id=ticket.event.id).exists():
                messages.error(request, 'Discount is not for this event!', 'error')
                return redirect('cart:confirm_cart', ord_id)

        order.discount = discount
        order.save()
        messages.success(request, 'Discount has been applied!', 'success')
        return redirect('cart:confirm_cart', ord_id)


class DeleteDiscountView(View):
    def get(self, request, ord_id):
        order = get_object_or_404(CartModel, id=ord_id)
        order.discount = None
        order.save()
        messages.success(request, 'Discount has been deleted!', 'success')
        return redirect('cart:confirm_cart', ord_id)
