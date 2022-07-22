from typing import List, Dict, Any, Optional
from mojang import MojangAPI

from .Skin import Skin


class User:
    def __init__(self, nickname: str | None, use_mojang_api: bool = True):
        self.nickname = nickname

        if self.nickname is not None:
            self.access = True

            if use_mojang_api:
                self.uuid = MojangAPI.get_uuid(nickname)

        else:
            self.uuid = None
            self.access = False

    def __str__(self):
        if self.nickname is None:
            return 'None'

        return self.nickname

    def get_skin(self) -> Optional[Skin]:
        if self.uuid is None:
            return None

        return Skin(self.uuid)

    def get_nickname_history(self) -> Optional[List[Dict[str, Any]]]:
        if self.uuid is None:
            return None

        return MojangAPI.get_name_history(self.uuid)
