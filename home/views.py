from django.shortcuts import render, redirect
from django.views import View
from events.models import Event

# Create your views here.

class HomeView(View):
    def get(self, request):
        events = Event.objects.order_by('created_at')[:6]
        return render(request, 'home/index.html', {'events': events})
