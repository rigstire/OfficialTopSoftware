# payments/urls.py
from django.urls import path
from .views import create_order, payment_success, payment_cancel

urlpatterns = [
    path('create-order/', create_order, name='create_order'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]