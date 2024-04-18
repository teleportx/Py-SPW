from typing import List

from ..methods.base import BaseMethod, RequestTypes
from ..models import Card


class GetUserCards(BaseMethod[List[Card]]):
    """
    Получает карты пользователя.

    https://github.com/sp-worlds/api-docs/wiki/%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BA%D0%B0%D1%80%D1%82-%D0%B8%D0%B3%D1%80%D0%BE%D0%BA%D0%B0
    """

    __returns__ = List[Card]
    __method__ = '/accounts/%s/cards'
    __request_type__ = RequestTypes.GET

    def __init__(self, username: str):
        super().__init__()
        self.__method__ %= username
