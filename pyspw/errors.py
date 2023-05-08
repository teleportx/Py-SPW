class _Error(Exception):
    pass


class _ApiError(_Error):
    pass


class SpwApiError(_ApiError):
    pass


class SpwApiDDOS(SpwApiError):
    def __init__(self):
        super().__init__("SPWorlds DDOS protection block your request")


class SpwUserNotFound(SpwApiError):
    def __init__(self, discord_id: str):
        self._discord_id = discord_id
        super().__init__(f"User with discord id `{discord_id}` not found in spworlds")

    @property
    def discord_id(self) -> str:
        return self._discord_id


class SpwUnauthorized(SpwApiError):
    def __init__(self):
        super().__init__("Access details are invalid")


class SpwInsufficientFunds(SpwApiError):
    def __init__(self):
        super().__init__("Insufficient funds on the card")


class SpwCardNotFound(SpwApiError):
    def __init__(self):
        super().__init__("Receiver card not found")


class MojangApiError(_ApiError):
    pass


class MojangAccountNotFound(MojangApiError):
    def __init__(self, nickname: str):
        self._nickname = nickname
        super().__init__(f"Account with name `{nickname}` not found")

    @property
    def nickname(self) -> str:
        return self._nickname


class SurgeplayApiError(_ApiError):
    pass


class LengthError(ValueError):
    def __init__(self, max_length: int):
        super().__init__(f"length must be <= {max_length}.")


class BigAmountError(ValueError):
    def __init__(self):
        super().__init__(f"amount must be <= 1728.")


class IsNotURLError(ValueError):
    def __init__(self):
        super().__init__(f"is not url.")


class IsNotCardError(ValueError):
    def __init__(self, card: str):
        super().__init__(f"Receiver card (`{card}`) number not valid")
