from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')
