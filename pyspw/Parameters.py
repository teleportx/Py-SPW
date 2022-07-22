class PaymentParameters:
    def __init__(self, amount: int, redirectUrl: str, webhookUrl: str, data: str):
        """
            Создание параметров ссылки на оплату
            :param amount: Стоимость покупки в АРах.
            :param redirectUrl: URL страницы, на которую попадет пользователь после оплаты.
            :param webhookUrl: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
            :param data: Строка до 100 символов, сюда можно помеcтить любые полезные данных.
            :return: Str ссылка на страницу оплаты, на которую стоит перенаправить пользователя.
        """

        self.amount = amount
        self.redirectUrl = redirectUrl
        self.webhookUrl = webhookUrl
        self.data = data

    def __str__(self):
        return f'''
                amount: {self.amount}
                redirectUrl: {self.redirectUrl}
                webhookUrl: {self.webhookUrl}
                data: {self.data}
               '''


class TransactionParameters:
    def __init__(self, receiver: str, amount: int, comment: str = 'No comment'):
        """
            Отправка транзакции
            :param receiver: Номер карты на которую будет совершена транзакция.
            :param amount: Сумма транзакции.
            :param comment: Комментарий к транзакции.
            :return: None.
        """

        self.receiver = receiver
        self.amount = amount
        self.comment = comment

    def __str__(self):
        return f'''
                receiver: {self.receiver}
                amount: {str(self.amount)}
                comment: {self.comment}
               '''