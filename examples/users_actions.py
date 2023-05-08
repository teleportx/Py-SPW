from typing import List

import pyspw
from pyspw.User import User, Skin

# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# get user by discord id
user: User = api.get_user('262632724928397312')

print(user.uuid)  # user uuid
print(user.nickname)  # user nickname

# working with user skin
skin: Skin = user.get_skin()

print(skin.variant)  # skin variant (slim or classic)
print(skin.get_head().get_url())  # get url of head
bust_image: bytes = skin.get_bust().get_image()  # get image (bytes) of skin bust


# Get more than one user
users: List[User] = api.get_users(['471286011851177994',
                                   '533953916082323456'], delay=0.4)

# print their uuids
for player in users:
    print(player.uuid)
