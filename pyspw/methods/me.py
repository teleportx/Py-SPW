from pyspw.methods.base import BaseMethod, RequestTypes
from pyspw.models import SelfUser


class Me(BaseMethod[SelfUser]):
    """
    Getting card owner information.

    https://github.com/sp-worlds/api-docs/wiki/%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-%D0%B2%D0%BB%D0%B0%D0%B4%D0%B5%D0%BB%D1%8C%D1%86%D0%B0-%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0
    """

    __returns__ = SelfUser
    __method__ = '/accounts/me'
    __request_type__ = RequestTypes.GET
