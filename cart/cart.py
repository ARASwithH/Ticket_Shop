from events.models import Event

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
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
