import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import StarletteHTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from internal.controller.http.v1.i18n_messages import (
    ONE_OR_MORE_FIELD_FAILED_TO_BE_VALIDATED_MESSAGE,
)
from internal.controller.http.v1.response import ErrorResponse
from internal.usecase.error_codes import (
    AUTHENTICATION_ERROR,
    DB_ERROR,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND_ERROR,
    PERMISSION_DENIED_ERROR,
    VALIDATION_ERROR,
)
from pkg import gettext
from pkg.exceptions import UNKNOWN_ERROR, TranslatableException
from pkg.i18n import Message

NUMBER_KEY = "_n"
USECASE_INPUT_VALIDATION_ERROR = "USECASE_INPUT_VALIDATION_ERROR"
ERROR_LOGGER_NAME = "gunicorn.error"

logger = logging.getLogger(ERROR_LOGGER_NAME)

__STATUS_CODE_MAP = {
    UNKNOWN_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    DB_ERROR: status.HTTP_406_NOT_ACCEPTABLE,
    NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
    VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
    USECASE_INPUT_VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
    INTERNAL_SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    AUTHENTICATION_ERROR: status.HTTP_401_UNAUTHORIZED,
    PERMISSION_DENIED_ERROR: status.HTTP_403_FORBIDDEN,
}
__LOG_FUNC_MAP = {
    UNKNOWN_ERROR: logger.error,
    DB_ERROR: logger.warning,
    NOT_FOUND_ERROR: logger.info,
    VALIDATION_ERROR: logger.info,
    USECASE_INPUT_VALIDATION_ERROR: logger.info,
    INTERNAL_SERVER_ERROR: logger.info,
    AUTHENTICATION_ERROR: logger.info,
    PERMISSION_DENIED_ERROR: logger.info,
}


def _log_exception(exc: Exception, code: str) -> None:
    log_func = __LOG_FUNC_MAP.get(code, logger.error)
    log_func(str(exc))


def _translate_func(message: Message, *args: Any, **kwargs: Any) -> str:  # noqa: ANN401
    number = kwargs.pop(NUMBER_KEY, 1)
    result = gettext.ngettext(message.singular, message.plural, number)
    return result.format(*args, **kwargs)


def _get_default_code(exc: Exception) -> str:
    code = getattr(exc, "code", UNKNOWN_ERROR)
    if code != UNKNOWN_ERROR:
        return code
    if isinstance(exc, (ValidationError, StarletteHTTPException)):
        code = USECASE_INPUT_VALIDATION_ERROR
    return code


async def exception_handler(_: Request, exc: Exception) -> JSONResponse:
    code = getattr(exc, "code", _get_default_code(exc))
    headers = getattr(exc, "headers", None)
    detail = getattr(exc, "detail", str(exc))
    message = ""

    if isinstance(exc, ValidationError):
        detail = exc.errors()
        exc = TranslatableException(
            exc, ONE_OR_MORE_FIELD_FAILED_TO_BE_VALIDATED_MESSAGE, _code=code
        )

    _log_exception(exc, code)
    status_code = getattr(
        exc,
        "status_code",
        __STATUS_CODE_MAP.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR),
    )

    if isinstance(exc, TranslatableException):
        message = exc.set_translate_func(_translate_func).__repr__()
    elif isinstance(exc, StarletteHTTPException):
        message = exc.detail or ""
    else:
        message = str(exc)

    return JSONResponse(
        content=ErrorResponse(message=message, code=code, detail=detail).dict(),
        status_code=status_code,
        headers=headers,
    )
