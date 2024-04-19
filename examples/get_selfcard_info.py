import pyspw

# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

card = api.card()

print(card.balance)  # Получаем баланс карты
print(card.webhook)  # Получаем адрес вебхука транзакций
