# payments/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import paypalrestsdk
import json
import logging
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)

# Debug logging for PayPal settings
logger.info(f"PayPal Mode: {settings.PAYPAL_MODE}")
logger.info(f"PayPal Client ID: {settings.PAYPAL_CLIENT_ID[:10]}...")
logger.info(f"PayPal Webhook URL: {settings.PAYPAL_WEBHOOK_URL}")

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def payments(request):
    """Render the payment page."""
    context = {
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'payments.html', context)

@csrf_exempt
def create_order(request):
    """Create a PayPal order."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        # Create PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"{settings.PAYPAL_WEBHOOK_URL}/payment/success/",
                "cancel_url": f"{settings.PAYPAL_WEBHOOK_URL}/payment/cancel/"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "description": "Payment for services"
            }]
        })

        if payment.create():
            logger.info(f"PayPal payment created successfully: {payment.id}")
            return JsonResponse({'orderID': payment.id})
        else:
            logger.error(f"PayPal payment creation failed: {payment.error}")
            return JsonResponse({'error': payment.error}, status=400)

    except Exception as e:
        logger.error(f"Error creating PayPal order: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def payment_success(request):
    """Handle successful payment."""
    return render(request, 'payments/success.html')

@csrf_exempt
def payment_cancel(request):
    """Handle canceled payment."""
    return render(request, 'payments/cancel.html')