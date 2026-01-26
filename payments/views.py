# payments/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import stripe
import json
import logging
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Debug logging for Stripe settings
logger.info(f"Stripe Secret Key configured: {settings.STRIPE_SECRET_KEY[:10]}...")
logger.info(f"Stripe Publishable Key: {settings.STRIPE_PUBLISHABLE_KEY[:10]}...")

def payments(request):
    """Render the payment page."""
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments.html', context)

@csrf_exempt
@require_POST
def create_payment_intent(request):
<<<<<<< HEAD
    """Create a Stripe Payment Intent or Subscription with Apple Pay support."""
    try:
        data = json.loads(request.body)
        amount = float(data.get('amount', 0))
        payment_type = data.get('payment_type', 'one_time')  # 'one_time' or 'monthly'
=======
    """Create a Stripe Payment Intent with Apple Pay support."""
    try:
        data = json.loads(request.body)
        amount = float(data.get('amount', 0))
>>>>>>> f8516ee003eb6f4fcd03e5ed9e2fec5a6cda3a08
        
        if amount < 0.50:  # Stripe minimum is $0.50
            return JsonResponse({'error': 'Amount must be at least $0.50'}, status=400)

        # Convert amount to cents for Stripe
        amount_cents = int(amount * 100)

<<<<<<< HEAD
        if payment_type == 'monthly':
            # Create a subscription for monthly payments
            try:
                # First, create a price for the subscription
                price = stripe.Price.create(
                    unit_amount=amount_cents,
                    currency='usd',
                    recurring={'interval': 'month'},
                    product_data={
                        'name': f'Monthly Subscription - ${amount:.2f}/month'
                    }
                )
                
                # Create a checkout session for subscription
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price': price.id,
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url=request.build_absolute_uri('/payments/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/payments/payment/cancel/'),
                    metadata={
                        'description': f'Monthly subscription for ${amount:.2f}/month'
                    }
                )
                
                logger.info(f"Stripe Subscription Checkout Session created: {checkout_session.id}")
                return JsonResponse({
                    'session_id': checkout_session.id,
                    'checkout_url': checkout_session.url,
                    'payment_type': 'subscription'
                })
            except stripe.error.StripeError as e:
                logger.error(f"Stripe subscription error: {str(e)}")
                return JsonResponse({'error': f'Subscription creation failed: {str(e)}'}, status=400)
        else:
            # Create one-time Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                automatic_payment_methods={
                    'enabled': True,
                },
                metadata={
                    'description': 'Payment for services'
                }
            )

            logger.info(f"Stripe Payment Intent created successfully with Apple Pay support: {intent.id}")
            return JsonResponse({
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'payment_type': 'one_time'
            })
=======
        # Create Payment Intent with automatic payment methods (includes Apple Pay, Google Pay, etc.)
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                'description': 'Payment for services'
            }
        )

        logger.info(f"Stripe Payment Intent created successfully with Apple Pay support: {intent.id}")
        return JsonResponse({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        })
>>>>>>> f8516ee003eb6f4fcd03e5ed9e2fec5a6cda3a08

    except stripe.error.CardError as e:
        logger.error(f"Stripe card error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    
    except stripe.error.RateLimitError as e:
        logger.error(f"Stripe rate limit error: {str(e)}")
        return JsonResponse({'error': 'Too many requests made to the API too quickly'}, status=429)
    
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Stripe invalid request error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    
    except stripe.error.AuthenticationError as e:
        logger.error(f"Stripe authentication error: {str(e)}")
        return JsonResponse({'error': 'Authentication with Stripe failed'}, status=401)
    
    except stripe.error.APIConnectionError as e:
        logger.error(f"Stripe API connection error: {str(e)}")
        return JsonResponse({'error': 'Network communication with Stripe failed'}, status=500)
    
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        logger.error(f"Error creating Stripe Payment Intent: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# Keep the old create_order endpoint for backwards compatibility
@csrf_exempt
def create_order(request):
    """Legacy endpoint that redirects to create_payment_intent."""
    return create_payment_intent(request)

@csrf_exempt
def payment_success(request):
<<<<<<< HEAD
    """Handle successful payment or subscription."""
    payment_intent_id = request.GET.get('payment_intent')
    session_id = request.GET.get('session_id')
=======
    """Handle successful payment."""
    payment_intent_id = request.GET.get('payment_intent')
>>>>>>> f8516ee003eb6f4fcd03e5ed9e2fec5a6cda3a08
    
    if payment_intent_id:
        try:
            # Verify the payment intent was successful
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == 'succeeded':
                logger.info(f"Payment confirmed successful: {payment_intent_id}")
            else:
                logger.warning(f"Payment intent status: {intent.status} for {payment_intent_id}")
        except Exception as e:
            logger.error(f"Error verifying payment intent: {str(e)}")
    
<<<<<<< HEAD
    if session_id:
        try:
            # Verify the checkout session was successful (for subscriptions)
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                logger.info(f"Subscription checkout confirmed successful: {session_id}")
                if session.mode == 'subscription':
                    logger.info(f"Subscription created: {session.subscription}")
        except Exception as e:
            logger.error(f"Error verifying checkout session: {str(e)}")
    
=======
>>>>>>> f8516ee003eb6f4fcd03e5ed9e2fec5a6cda3a08
    return render(request, 'payments/success.html')

@csrf_exempt
def payment_cancel(request):
    """Handle canceled payment."""
    return render(request, 'payments/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.warning("Stripe webhook secret not configured")
        return JsonResponse({'error': 'Webhook secret not configured'}, status=400)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.info(f"Payment succeeded: {payment_intent['id']}")
        # Handle successful payment here (e.g., fulfill order, send confirmation email)
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logger.info(f"Payment failed: {payment_intent['id']}")
        # Handle failed payment here
    
    else:
        logger.info(f"Unhandled event type: {event['type']}")

    return JsonResponse({'status': 'success'})