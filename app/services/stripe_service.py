import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

async def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Magical Creature',
                            'description': 'Your unique magical creature',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )
        return checkout_session
    except Exception as e:
        raise ValueError(str(e))

async def get_session_status(session_id: str):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except Exception as e:
        raise ValueError(str(e))

