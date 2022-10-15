from fastapi import Request, status
from fastapi.responses import JSONResponse

from internal.controller.http.v1.response import ErrorResponse
from internal.usecase.error_codes import (
    AUTHENTICATION_ERROR,
    DB_ERROR,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND_ERROR,
    PERMISSION_DENIED_ERROR,
    VALIDATION_ERROR,
)
from pkg.exceptions import UNKNOWN_ERROR, TranslatableException

__STATUS_CODE_MAP = {
    UNKNOWN_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    DB_ERROR: status.HTTP_406_NOT_ACCEPTABLE,
    NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
    VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
    INTERNAL_SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    AUTHENTICATION_ERROR: status.HTTP_401_UNAUTHORIZED,
    PERMISSION_DENIED_ERROR: status.HTTP_403_FORBIDDEN,
}


def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    code = getattr(exc, "code", UNKNOWN_ERROR)
    status_code = __STATUS_CODE_MAP.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    message = ""

    if isinstance(exc, TranslatableException):
        pass
    else:
        pass

    return JSONResponse(
        context=ErrorResponse(message=message, code=code).dict(),
        status_code=status_code,
    )
