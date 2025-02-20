from django.urls import path
from .views import process_payment, payment_view

urlpatterns = [
    path("process-payment/", process_payment, name="process_payment"),
    path("payments/", payment_view, name="payments")
]