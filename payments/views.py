import logging
from square.client import Client
from django.conf import settings
from django.http import JsonResponse
import uuid
import json
from django.shortcuts import render

logger = logging.getLogger(__name__)

def process_payment(request):
    if request.method == "POST":
        try:
            client = Client(access_token=settings.SQUARE_ACCESS_TOKEN, environment="production")
            data = json.loads(request.body)

            # Log request data
            logger.info(f"Received Payment Request: {data}")

            # Validate amount and sourceId
            if "amount" not in data or "sourceId" not in data:
                return JsonResponse({"status": "error", "message": "Missing amount or sourceId"}, status=400)

            amount_in_cents = int(data["amount"])  # Amount should be in cents
            source_id = data["sourceId"]  # Payment token from Square frontend

            if amount_in_cents <= 0:
                return JsonResponse({"status": "error", "message": "Invalid amount"}, status=400)

            payment_body = {
                "idempotency_key": str(uuid.uuid4()),  # Prevent duplicate payments
                "source_id": source_id,  # Payment token from frontend
                "amount_money": {
                    "amount": amount_in_cents,  # Amount in cents
                    "currency": "USD"
                }
            }

            # Log the payment request body
            logger.info(f"Payment Request to Square: {payment_body}")

            response = client.payments.create_payment(payment_body)

            if response.is_success():
                return JsonResponse({"status": "success", "payment_id": response.body["payment"]["id"]})
            else:
                # Log the full error details from Square API
                error_details = response.errors if response.errors else "Unknown error"
                logger.error(f"Square API Error: {error_details}")
                return JsonResponse({"status": "error", "message": error_details}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def payment_view(request):
    return render(request, "payments.html")