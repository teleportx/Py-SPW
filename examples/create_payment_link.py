import json

import pyspw
from pyspw.models import Payment


# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Constructing payment
payment = Payment(
    amount=150,  # Payment amount (You can't set more than one shulker diamond ore)
    redirectUrl='https://spwdev.xyz/',  # URL which redirects user after successful payment
    webhookUrl='https://spwdev.xyz/api/webhook_spw',  # URL which receive webhook of successful payment with data
    data=json.dumps({  # Useful data which received with webhook on webhookUrl
        "type": "prepayment",
        "order": 987951455
    })
)

# Create payment link
print(api.create_payment(payment))


# Create more than one payment link
prepayment = Payment(
    amount=150,
    redirectUrl='https://spwdev.xyz/',
    webhookUrl='https://spwdev.xyz/api/webhook_spw',
    data=json.dumps({
        "type": "prepayment",
        "order": 987951455
    })
)

# clone similar payment
post_payment = prepayment
post_payment.data = json.dumps({  # You can access to payment variables
        "type": "post-payment",
        "order": 987951455
    })


# Create payment links
api.create_payments([prepayment, post_payment], delay=0.6)
# !Payments links valid for 5 minutes!
