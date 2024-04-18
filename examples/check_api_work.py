import pyspw

# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Проверяем
print(api.ping())
