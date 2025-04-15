import logging
import stripe
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
    
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


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
