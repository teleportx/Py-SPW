import pyspw


# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

# Check access to server
print(api.check_access('287598524017803264'))  # True
print(api.check_access('289341856083607552'))  # False


# Check more than one access
print(api.check_accesses(['403987036219899908', '558667431187447809'], delay=1))  # False, True
