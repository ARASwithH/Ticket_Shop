from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import EventForm
from .models import Event
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event created.')
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Your event has been updated.')
        return super().form_valid(form)

