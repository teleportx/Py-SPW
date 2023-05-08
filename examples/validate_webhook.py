import json

import pyspw

# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Data received from webhook
webhook_body = {
    "payer": "Nakke_",
    "amount": 10,
    "data": "brax10"
}
X_Body_Hash = "fba3046f2800197d8829556bdf2d04bf61a307d4ede31eb37fb4078d21e24d3e"

# Verify
print(api.check_webhook(json.dumps(webhook_body), X_Body_Hash))  # True or False
