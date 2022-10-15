from typing import Any, Callable, Optional

from pkg.i18n import Message

UNKNOWN_ERROR = "UNKNOWN"


class TranslatableException(Exception):
    def __init__(
        self,
        inner_exception: Exception,
        i18n_message: Optional[Message],
        *format_args: Any,  # noqa: ANN401
        _code: str = UNKNOWN_ERROR,
        _translate_func: Optional[Callable[..., str]] = None,
        **format_kwargs: Any,  # noqa: ANN401
    ) -> None:
        self._code = _code
        self._inner_exception = inner_exception
        self.__i18n_message = i18n_message
        self.__translate_func = _translate_func
        self.__format_args = format_args
        self.__format__kwargs = format_kwargs

    @property
    def code(self) -> str:
        return self._code

    def unwrap(self) -> Exception:
        return self._inner_exception

    def set_translate_func(self, func: Callable[..., str]) -> None:
        self.__translate_func = func

    @property
    def display_message(self) -> str:
        msg = ""
        if self.__translate_func is not None and self.__i18n_message is not None:
            msg = self.__translate_func(
                self.__i18n_message, *self.__format_args, **self.__format__kwargs
            )
        if msg:
            return msg
        if self.__i18n_message is not None:
            return self.__i18n_message.singular
        return str(self)

    def __str__(self) -> str:
        return str(self._inner_exception)

    def __repr__(self) -> str:
        return self.display_message
