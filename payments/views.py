import logging
import stripe
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt  # Only use this if CSRF is an issue during development/testing
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            logger.info(f"Received Stripe Payment Request: {data}")

            if "amount" not in data or "payment_method_id" not in data:
                return JsonResponse({"status": "error", "message": "Missing amount or payment_method_id"}, status=400)

            amount_in_cents = int(data["amount"])
            payment_method_id = data["payment_method_id"]

            if amount_in_cents <= 0:
                return JsonResponse({"status": "error", "message": "Invalid amount"}, status=400)

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True
            )

            return JsonResponse({"status": "success", "payment_intent_id": intent.id})

        except stripe.error.CardError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Stripe Payment Error: {str(e)}")
            return JsonResponse({"status": "error", "message": "Payment processing failed"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def payment_view(request):
    return render(request, "payments.html")