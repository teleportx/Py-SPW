class Error(Exception):
    pass


class WebserverError(Error):
    pass


class NotFunction(WebserverError):
    pass


class ApiError(Error):
    pass


class SpwApiError(ApiError):
    pass


class BadParameter(SpwApiError):
    pass


class MojangApiError(ApiError):
    pass


class SurgeplayApiError(ApiError):
    pass


class BadSkinPartName(SurgeplayApiError):
    pass
