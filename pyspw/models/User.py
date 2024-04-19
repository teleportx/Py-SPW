from datetime import datetime
from enum import Enum
from typing import Optional, List
from warnings import warn

import requests as rq
from mojang import API as MAPI
from mojang._types import UserProfile
from pydantic import BaseModel, computed_field

from . import Card
from .. import errors as err

mapi = MAPI()


class SkinVariant(Enum):
    """
    Варианты скинов.
    """
    SLIM = 'slim'
    CLASSIC = 'classic'


class _SkinPart:
    def __init__(self, url: str):
        self.__skin_part_url = url

    def __str__(self):
        return self.get_url()

    def __bytes__(self):
        return self.get_image()

    def get_url(self) -> str:
        """
        Получения ссылки на изображение части скина.

        :return: Ссылка на изображение части скина.
        """
        return self.__skin_part_url

    def get_image(self) -> bytes:
        """
        Получения изображения части скина.

        :return: Изображения части скина.
        """

        try:
            visage_surgeplay_response = rq.get(self.__skin_part_url)
            if visage_surgeplay_response.status_code != 200:
                raise err.SurgeplayApiError(f'HTTP status: {visage_surgeplay_response.status_code}')
            return visage_surgeplay_response.content

        except rq.exceptions.ConnectionError as error:
            raise err.SurgeplayApiError(error)


class Skin:
    __visage_surgeplay_url = 'https://visage.surgeplay.com/'

    def __init__(self, profile: UserProfile):
        self._profile = profile
        self._variant = SkinVariant(profile.skin_variant)

    @property
    def variant(self) -> SkinVariant:
        return self._variant

    @property
    def cape(self) -> Optional[_SkinPart]:
        if self._profile.cape_url is None:
            return None
        return _SkinPart(self._profile.cape_url)

    def get_face(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/face/{image_size}/{self._profile.id}')

    def get_front(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/front/{image_size}/{self._profile.id}')

    def get_front_full(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/frontfull/{image_size}/{self._profile.id}')

    def get_head(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/head/{image_size}/{self._profile.id}')

    def get_bust(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/bust/{image_size}/{self._profile.id}')

    def get_full(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/full/{image_size}/{self._profile.id}')

    def get_skin(self, image_size: int = 64) -> _SkinPart:
        return _SkinPart(f'https://visage.surgeplay.com/skin/{image_size}/{self._profile.id}')


class City(BaseModel):
    id: str
    name: str
    description: str

    x: int
    z: int
    isMayor: bool


class User(BaseModel):
    username: Optional[str]
    uuid: Optional[str]

    @property
    def nickname(self) -> Optional[str]:
        warn('Use .username', DeprecationWarning)
        return self.username

    def get_profile(self) -> Optional[UserProfile]:
        if self.uuid is None:
            return

        return mapi.get_profile(self.uuid)

    def get_skin(self) -> Skin:
        return Skin(self.get_profile())


class SelfUser(BaseModel):
    id: str
    username: str

    @computed_field
    @property
    def uuid(self) -> Optional[str]:
        if not hasattr(self, '__uuid'):
            self.__uuid = mapi.get_uuid(self.username)
        return self.__uuid

    status: str
    city: Optional[City]

    roles: List[str]
    cards: List[Card]

    createdAt: datetime
