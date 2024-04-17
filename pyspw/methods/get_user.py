from pyspw.methods.base import BaseMethod, RequestTypes
from pyspw.models import User


class GetUser(BaseMethod[User]):
    """
    Получает информацию о пользователе: ник, uuid и т.д.

    https://github.com/sp-worlds/api-docs/wiki/%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%B8%D0%BA%D0%B0-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F
    """

    __returns__ = User
    __method__ = '/users/%s'
    __request_type__ = RequestTypes.GET

    def __init__(self, discord_id: int):
        super().__init__()
        self.__method__ %= discord_id
        