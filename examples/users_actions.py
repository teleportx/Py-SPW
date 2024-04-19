from typing import List

import pyspw
from pyspw.models import User, Skin

# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Получаем пользователя с помощью айди
user: User = api.get_user('262632724928397312')

print(user.uuid)  # Получаем uuid
print(user.nickname)  # Получаем ник

# Работаем со скинами пользователя
skin: Skin = user.get_skin()

print(skin.variant)                              # получаем вариант скина (slim или classic)
print(skin.get_head().get_url())                 # Получаем адрес картинки скина с головой
bust_image: bytes = skin.get_bust().get_image()  # Получаем изображение (bytes) всего скина


# Получаем больше чем одного пользователя
users: List[User] = api.get_users(['471286011851177994',
                                   '533953916082323456'], delay=0.4)

# Выводим их uuid
for player in users:
    print(player.uuid)
