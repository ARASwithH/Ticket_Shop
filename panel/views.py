from django.shortcuts import render
from django.views.generic import ListView, View
from events.models import Event

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
    pass


class PaymentsView(ListView):
    pass


class OrdersView(ListView):
    pass


class AlterAccountView(View):
    pass
