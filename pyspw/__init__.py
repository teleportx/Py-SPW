from . import api
from . import errors

__all__ = ["Api", "errors"]
__version__ = 1.0


class Api(api.sp_api_base):
    pass
