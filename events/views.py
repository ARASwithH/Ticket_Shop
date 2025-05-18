from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import EventForm, AddCartForm
from .models import Event, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



# Create your views here.

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        # Ordering
        order_by = self.request.GET.get('order_by')
        if order_by == 'price_asc':
            queryset = queryset.order_by('price_per_ticket')
        elif order_by == 'price_desc':
            queryset = queryset.order_by('-price_per_ticket')
        elif order_by == 'newest':
            queryset = queryset.order_by('start_date')
        elif order_by == 'oldest':
            queryset = queryset.order_by('-start_date')

        # Filter by category
        categories = self.request.GET.getlist('category')
        if categories:
            queryset = queryset.filter(category__slug__in=categories).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category')  # ✅ add this
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context['event']
        context['form'] = AddCartForm(capacity=event.capacity)
        return context




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

