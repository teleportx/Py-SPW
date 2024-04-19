import platform
from abc import ABC
from enum import Enum
from typing import TypeVar, Generic, List, Tuple

import requests as rq
from pydantic import BaseModel

from .. import errors as err

SPWORLDS_API_HOST = 'https://spworlds.ru/api/public'

ReturnType = TypeVar('ReturnType', BaseModel, List[BaseModel])


class RequestTypes(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'


class BaseMethod(ABC, Generic[ReturnType]):
    __returns__: ReturnType
    __method__: str
    __request_type__: RequestTypes

    def __init__(self, **kwargs):
        self._body = kwargs

    def _request(self, authorization: str) -> rq.Response:
        headers = {
            'Authorization': authorization,
            'User-Agent': f'Py-SPW (Python {platform.python_version()})'
        }

        try:
            response = rq.request(
                self.__request_type__.value,
                url=SPWORLDS_API_HOST + self.__method__,
                headers=headers,
                json=self._body
            )

        except rq.exceptions.ConnectionError as error:
            raise err.SpwApiError(0, error.strerror)

        # Verifying DDOS
        try:
            response.json()

        except rq.exceptions.JSONDecodeError:
            raise err.SpwApiDDOS()

        # Verifying status codes
        if response.ok:
            return response

        elif response.status_code == 401:
            raise err.SpwUnauthorized()

        elif response.status_code >= 500:
            raise err.SpwApiError(response.status_code, extra_info='Remote server error.')

        else:
            raise err.SpwApiError(response.status_code, response.json().get('error'), response.json().get('message'))

    def __call__(self, authorization: str) -> ReturnType:
        if hasattr(self.__returns__, '__args__') and \
                isinstance(self.__returns__.__args__, Tuple) and \
                len(self.__returns__.__args__) > 0 and \
                self.__returns__ == List[self.__returns__.__args__[0]]:
            res = []
            for el in self._request(authorization).json():
                res.append(self.__returns__.__args__[0].model_validate(el))

            return res

        return self.__returns__.model_validate_json(self._request(authorization).text)
