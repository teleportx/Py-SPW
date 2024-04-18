import pyspw
from pyspw.models import Transaction


# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Собираем транзакцию
transaction = Transaction(
    receiver='00001',              # Номер карты получателя
    amount=24,                     # Сумма, которую вы хотите отправить
    comment='Buy diamond pickaxe'  # Комментарий для транзакции
)

# Отправляем транзакцию
api.send_transaction(transaction)


# Отправляем больше чем одну транзакцию
salary = Transaction(
    receiver='00002',
    amount=100,
    comment='Salary for the January'
)

# Вы можете получать информацию о транзакции из класса
tax = Transaction(
    receiver='00001',
    amount=round(salary.amount * 0.2),  # берем 20% с зарплаты
    comment=f'Tax from `{salary.comment}`'
)

# Отправляем транзакции
api.send_transactions([tax, salary], delay=0.8)
