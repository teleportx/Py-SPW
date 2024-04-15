import pyspw
from pyspw.models import Transaction


# Init library
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')


# Constructing transaction
transaction = Transaction(
    receiver='00001',  # Card number of receiver
    amount=24,  # Amount of diamond ore which you want to send
    comment='Buy diamond pickaxe'  # Comment on transaction
)

# Send transaction
api.send_transaction(transaction)


# Send more than one transaction
salary = Transaction(
    receiver='00002',
    amount=100,
    comment='Salary for the January'
)


# You can get information from Transaction class
tax = Transaction(
    receiver='00001',
    amount=round(salary.amount * 0.2),  # take 20% from salary amount
    comment=f'Tax from `{salary.comment}`'
)

# Send transactions
api.send_transactions([tax, salary], delay=0.8)
