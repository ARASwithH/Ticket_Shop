from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from events.models import Event
from events.forms import AddCartForm


# Create your views here.

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        print(cart.cart.keys())
        print(cart.cart.values())
        return render(request, 'cart/cart_view.html', {'cart': cart})


class AddCartView(View):
    def post(self, request, ev_id):
        cart = Cart(request)
        event = get_object_or_404(Event, id=ev_id)
        form = AddCartForm(request.POST)

        if form.is_valid():
            cart.add(event, form.cleaned_data['quantity'])
            # print(cart.cart.keys())
            # print(cart.cart.values())
            return redirect('cart:cart_view')

