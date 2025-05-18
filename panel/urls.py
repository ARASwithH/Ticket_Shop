from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('tickets/', views.TicketsView.as_view(), name='tickets'),
    path('payments/', views.PaymentsView.as_view(), name='payments'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
]