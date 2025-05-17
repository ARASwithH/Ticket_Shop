from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('events/', views.EventsView.as_view(), name='events'),
]