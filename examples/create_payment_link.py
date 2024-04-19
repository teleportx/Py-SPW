import json

import pyspw
from pyspw.models import Payment, PaymentItem

# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Собираем платеж
payment = Payment(
    redirectUrl='https://spworlds.city/',                # Адрес куда перенаправит пользователя после оплаты
    webhookUrl='https://spworlds.city/api/webhook_spw',  # Адрес куда придет вебхук об успешной оплате
    data=json.dumps({                                    # Любая полезная вам информация, будет получена вместе с бехуком
        "type": "prepayment",
        "order": 987951455
    }),
    items=[                                              # Товары на которые оформляет платеж пользователь
        PaymentItem(
            name='Aboba',                 # Название товара
            count=10,                     # Количество
            price=32,                     # Цена за 1 штуку
            comment='Абоба обыкновенная'  # Комментарий к товару (необязательно)
        ),
        PaymentItem(
            name='Боба',
            count=1,
            price=48
        ),
    ]
)

# Создать ссылку на оплату
print(api.create_payment(payment))


# Создать много ссылок на оплату
api.create_payments([payment, payment], delay=0.6)
# ! Ссылки на оплату валидны 5 минут !
