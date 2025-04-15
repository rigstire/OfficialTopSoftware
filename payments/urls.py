from django.urls import path
from .views import  payment_view, paypal_confirm

urlpatterns = [
    path("payments/", payment_view, name="payments"),
     path('paypal-confirm/', paypal_confirm, name='paypal_confirm'),
]