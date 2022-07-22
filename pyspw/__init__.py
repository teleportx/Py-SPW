from . import api
from . import errors
from . import User
from . import Skin
from . import Parameters

__all__ = ["SpApi", "errors", "User", "Skin"]


class SpApi(api.Py_SPW):
    pass
