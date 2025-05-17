from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_view'),
    path('add/<int:ev_id>/', views.AddCartView.as_view(), name='add_cart'),
    path('remove/<int:ev_id>/', views.RemoveCartView.as_view(), name='remove_cart'),
    path('confirm/<int:ord_id>/', views.ConfirmCartView.as_view(), name='confirm_cart'),
    # path('apply-discount/', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('creat_order/', views.CreatOrderView.as_view(), name='creat_order'),

]