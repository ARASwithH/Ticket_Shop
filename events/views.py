from django.shortcuts import render
from django.views.generic import ListView
from .models import Event

# Create your views here.

class IndexView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6
