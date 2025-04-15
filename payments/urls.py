from django.urls import path
from .views import process_payment, payment_view, paypal_confirm

urlpatterns = [
    path("process-payment/", process_payment, name="process_payment"),
    path("payments/", payment_view, name="payments"),
     path('paypal-confirm/', paypal_confirm, name='paypal_confirm'),
]