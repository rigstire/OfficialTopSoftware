from square.client import Client
from django.conf import settings
from django.http import JsonResponse
import uuid
import json
from django.shortcuts import render

# Initialize Square client
client = Client(access_token=settings.SQUARE_ACCESS_TOKEN, environment="sandbox")

def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount_in_cents = int(data.get("amount"))  # Get total amount from frontend

            if amount_in_cents <= 0:
                return JsonResponse({"status": "error", "message": "Invalid amount"}, status=400)

            body = {
                "idempotency_key": str(uuid.uuid4()),  # Prevent duplicate payments
                "source_id": data.get("nonce"),  # Payment token from frontend
                "amount_money": {
                    "amount": amount_in_cents,  # Amount in cents
                    "currency": "USD"
                }
            }

            response = client.payments.create_payment(body)

            if response.is_success():
                return JsonResponse({"status": "success", "payment_id": response.body["payment"]["id"]})
            else:
                return JsonResponse({"status": "error", "message": response.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
def payment_view(request):
    return render(request, "payments.html")  # Ensure payments.html exists in your templates folder
