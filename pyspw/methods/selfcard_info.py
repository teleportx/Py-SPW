from pyspw.methods.base import BaseMethod, RequestTypes
from pyspw.models import SelfCard


class GetSelfCardInfo(BaseMethod[SelfCard]):
    """
    Получает информацию о текущей карте: баланс, вебхук операций.

    https://github.com/sp-worlds/api-docs/wiki/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%BE-%D0%BA%D0%B0%D1%80%D1%82%D0%B5
    """

    __returns__ = SelfCard
    __method__ = '/card'
    __request_type__ = RequestTypes.GET
