from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from events.models import Event
from events.forms import AddCartForm
from accounts.models import User
from accounts.forms import UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PaymentMethodForm


# Create your views here.

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_view.html', {'cart': cart})


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
    def get(self, request):
        user = request.user
        form1 = UserUpdateForm(instance=user)
        form2 = PaymentMethodForm()
        cart = Cart(request)
        return render(request, 'cart/final_view.html', {'form1': form1,
                                                        'form2': form2,
                                                        'cart': cart})

    def post(self, request):
        user = request.user
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = PaymentMethodForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            pay_method = form2.cleaned_data['payment_methods']
            if pay_method == 'paypal':
                print(pay_method)
            if pay_method == 'credit':
                print(pay_method)
            if pay_method == 'cash':
                print(pay_method)
            return redirect('home:home')
        return render(request, 'cart/final_view.html', {'form1': form1,
                                                        'form2': form2,})
