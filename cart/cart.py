from events.models import Event
from .models import Payment, Ticket, CartModel

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        cart = self.session.get('CART_SESSION_ID')
        if not cart:
            cart = self.session['CART_SESSION_ID'] = {}
        self.cart = cart

    def __iter__(self):
        event_ids = self.cart.keys()
        events = Event.objects.filter(id__in=event_ids)
        cart = self.cart.copy()
        for event in events:
            cart[str(event.id)]['event'] = event

        for item in cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])
            yield item

    def add(self, event, quantity):
        event_id = str(event.id)
        if event_id not in self.cart:
            self.cart[event_id] = {
                'quantity': 0,
                'price': str(event.price_per_ticket),
            }
        self.cart[event_id]['quantity'] += quantity
        self.save()

    def remove(self, event):
        event_id = str(event.id)
        if event_id in self.cart:
            del self.cart[event_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        total_price = 0
        for event in self:
            total_price += event['total_price']
        return total_price

    def clear(self):
        self.session['CART_SESSION_ID'] = {}
        self.save()

    def save_payment_info(self, payment_method, total_price, status='complete'):

        Payment.objects.create(
            from_user=self.user,
            amount=total_price,
            payment_method=payment_method,
            status=status
        )

    def save_tickets(self):
        event_ids = self.cart.keys()
        events = Event.objects.filter(id__in=event_ids)
        tickets = []

        for item in events:
            ticket = Ticket.objects.create(
                user=self.user,
                event=item,
                quantity=self.cart[f'{item.id}']['quantity'],
            )
            tickets.append(ticket)

        return tickets

    def save_cart(self, tickets):
        cart = CartModel.objects.create(
            user=self.user,
            total_price=self.get_total_price(),
        )
        for item in tickets:
            cart.tickets.add(item)

        return cart






