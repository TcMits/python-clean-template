from typing import Callable

UNKNOWN_ERROR = "UNKNOWN"


class TranslatableError(Exception):
    _translate_func: Callable[..., str]

    def __init__(
        self,
        message: str,
        translate_key: str,
        default_translated_message: str,
        *,
        code: str = UNKNOWN_ERROR,
    ) -> None:
        self._message = message
        self._translate_key = translate_key
        self._default_translated_message = default_translated_message
        self._code = code

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    @property
    def translate_key(self) -> str:
        return self._translate_key

    @property
    def default_translated_message(self) -> str:
        return self._default_translated_message

    def display_message(self) -> str:
        pass

    def __str__(self) -> str:
        return self._message

    def __repr__(self) -> str:
        return super().__repr__()
