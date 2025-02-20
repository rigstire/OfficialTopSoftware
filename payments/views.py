# payments/views.py
from django.shortcuts import render

def payment_view(request):
    return render(request, 'payments/payment.html')
