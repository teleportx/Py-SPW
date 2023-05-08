import pyspw

# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

# Get card balance
print(api.get_balance())
