from django.urls import path
from .views import  payment_view, paypal_confirm, create_order, paypal_webhook

urlpatterns = [
    path("payments/", payment_view, name="payments"),
    path('paypal-confirm/', paypal_confirm, name='paypal_confirm'),
    path('create_order/', create_order, name='create_order'  ),
    path('paypal_webhook',paypal_webhook, name="paypal_webhook")
]