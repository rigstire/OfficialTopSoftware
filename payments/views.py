import logging
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import paypalrestsdk
import json

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@csrf_exempt  # Only for testing - use proper CSRF protection in production
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            
            # Create PayPal payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": amount,
                        "currency": "USD"
                    },
                    "description": "Website Development Payment"
                }],
                "redirect_urls": {
                    "return_url": "https://topsoftware.tech/",
                    "cancel_url": "https://topsoftware.tech/"
                }
            })
            
            if payment.create():
                return JsonResponse({'orderID': payment.id})
            else:
                return JsonResponse({'error': payment.error}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
logger = logging.getLogger(__name__)


def payment_view(request):
    return render(request, "payments.html")

@csrf_exempt
def paypal_confirm(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"PayPal confirmation: {data}")
            return JsonResponse({"status": "success"})
        except Exception as e:
            logger.error(f"PayPal confirm error: {e}")
            return JsonResponse({"status": "error", "message": "Server error"}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)
