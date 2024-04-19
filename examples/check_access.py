import pyspw


# Инициализация класса
api = pyspw.SpApi(card_id='card_id',
                  card_token='card_token')

# Проверяем доступ к серверу
print(api.check_access('287598524017803264'))  # True
print(api.check_access('289341856083607552'))  # False


# Проверяем множество айди
print(api.check_accesses(['403987036219899908', '558667431187447809'], delay=1))  # False, True
