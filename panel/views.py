from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

# Create your views here.

class IndexView(View):
    def get(self, request, id):
        return render(request, 'panel/index.html')


class EventsView(ListView):
    pass


class TicketsView(ListView):
    pass


class PaymentsView(ListView):
    pass


class OrdersView(ListView):
    pass


class AlterAccountView(View):
    pass
