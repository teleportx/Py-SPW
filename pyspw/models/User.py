from datetime import datetime
from enum import Enum
from typing import Optional, List
from warnings import warn

import requests as rq
from mojang import API as MAPI
from mojang._types import UserProfile
from pydantic import BaseModel, computed_field, Field

from . import Card
from .. import errors as err

mapi = MAPI()


class SkinVariant(Enum):
    """
    Варианты скинов.
    """
    SLIM = 'slim'
    CLASSIC = 'classic'


class SkinPart:
    def __init__(self, url: str):
        self.__skin_part_url = url

    @property
    def url(self) -> str:
        """
        Адрес изображения части скина.
        """

        return self.__skin_part_url

    def get_url(self) -> str:
        warn('Use .url', DeprecationWarning)

        return self.url

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
    def cape(self) -> Optional[SkinPart]:
        if self._profile.cape_url is None:
            return None
        return SkinPart(self._profile.cape_url)

    def get_face(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/face/{image_size}/{self._profile.id}')

    def get_front(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/front/{image_size}/{self._profile.id}')

    def get_front_full(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/frontfull/{image_size}/{self._profile.id}')

    def get_head(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/head/{image_size}/{self._profile.id}')

    def get_bust(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/bust/{image_size}/{self._profile.id}')

    def get_full(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/full/{image_size}/{self._profile.id}')

    def get_skin(self, image_size: int = 64) -> SkinPart:
        return SkinPart(f'https://visage.surgeplay.com/skin/{image_size}/{self._profile.id}')


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
    uuid: Optional[str] = Field(validation_alias='minecraftUUID')

    status: str
    city: Optional[City]

    roles: List[str]
    cards: List[Card]

    createdAt: datetime
