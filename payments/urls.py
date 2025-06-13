# payments/urls.py
from django.urls import path
from .views import create_order, create_payment_intent, payment_success, payment_cancel, payments, stripe_webhook

urlpatterns = [
    path('create-order/', create_order, name='create_order'),  # Legacy endpoint
    path('create-payment-intent/', create_payment_intent, name='create_payment_intent'),  # New Stripe endpoint
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
    path('payments/payments', payments, name="payments"),
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),
]