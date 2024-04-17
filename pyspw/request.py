import platform
from enum import Enum

import requests as rq

from . import errors as err


SPWORLDS_API_HOST = 'https://spworlds.ru/api/public'

class _RequestTypes(Enum):
    POST = 'POST'
    GET = 'GET'


def request(method: _RequestTypes, authorization: str, path: str = '', body: dict = None, *,
             ignore_codes=None) -> rq.Response:
    if ignore_codes is None:
        ignore_codes = []

    headers = {
        'Authorization': authorization,
        'User-Agent': f'Py-SPW (Python {platform.python_version()})'
    }
    try:
        response = rq.request(method.value, url=SPWORLDS_API_HOST + path, headers=headers, json=body)

    except rq.exceptions.ConnectionError as error:
        raise err.SpwApiError(error)

    if response.headers.get('Content-Type') != 'application/json':
        raise err.SpwApiDDOS()

    if response.ok or response.status_code in ignore_codes:
        return response

    elif response.status_code == 401:
        raise err.SpwUnauthorized()

    elif response.status_code >= 500:
        raise err.SpwApiError(f'HTTP: {response.status_code}, Server Error.')

    else:
        raise err.SpwApiError(
            f'HTTP: {response.status_code} {response.json()["error"]}. Message: {response.json()["message"]}')