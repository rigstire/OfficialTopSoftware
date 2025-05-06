# payments/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            
            # Validate amount
            try:
                amount_float = float(amount)
                if amount_float < 1.00:  # Minimum $1.00
                    return JsonResponse({'error': 'Minimum payment is $1.00'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid amount'}, status=400)

            # Create PayPal payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": "{:.2f}".format(amount_float),
                        "currency": "USD"
                    },
                    "description": "Website Development Service"
                }],
                "redirect_urls": {
                    "return_url": "https://yourdomain.com/payment/success/",
                    "cancel_url": "https://yourdomain.com/payment/cancel/"
                }
            })

            if payment.create():
                logger.info(f"PayPal payment created: {payment.id}")
                return JsonResponse({
                    'orderID': payment.id,
                    'status': payment.state
                })
            else:
                error_msg = payment.error.get('message', 'Payment creation failed')
                logger.error(f"PayPal error: {error_msg}")
                return JsonResponse({'error': error_msg}, status=400)

        except Exception as e:
            logger.error(f"Payment error: {str(e)}")
            return JsonResponse({'error': 'Server error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=405)

@csrf_exempt
def payment_success(request):
    # Handle successful payment (save to database, send email, etc.)
    return render(request, 'payments/success.html')

@csrf_exempt
def payment_cancel(request):
    # Handle canceled payment
    return render(request, 'payments/cancel.html')