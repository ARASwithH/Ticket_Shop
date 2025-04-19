from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('registration/verify/', views.UserVerifyView.as_view(), name='verify'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login/send_code/', views.UserSendCodeView.as_view(), name='send_code'),
    path('login/send_code/verify/', views.UserLoginVerifyView.as_view(), name='send_code_verify'),
]
