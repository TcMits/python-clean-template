import json
from typing import Dict, List

from fastapi import status
from fastapi.exceptions import StarletteHTTPException
from pydantic import ValidationError

from internal.controller.http.v1.exceptions import (
    USECASE_INPUT_VALIDATION_ERROR,
    exception_handler,
)
from internal.controller.http.v1.i18n_messages import (
    ONE_OR_MORE_FIELD_FAILED_TO_BE_VALIDATED_MESSAGE,
)
from pkg.exceptions import UNKNOWN_ERROR


def test_exception_handler_with_validation_error():
    class FakeValidationError(ValidationError):
        def __init__(self) -> None:
            pass

        def errors(self):
            return [{"msg": "test"}]

        def __str__(self) -> str:
            return "test"

    resp = exception_handler(None, FakeValidationError())

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(resp.body.decode("utf-8")) == {
        "message": ONE_OR_MORE_FIELD_FAILED_TO_BE_VALIDATED_MESSAGE.singular,
        "code": USECASE_INPUT_VALIDATION_ERROR,
        "detail": [{"msg": "test"}],
    }


def test_exception_handler_with_http_exception():
    exc = StarletteHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="test")
    resp = exception_handler(None, exc)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert json.loads(resp.body.decode("utf-8")) == {
        "message": "test",
        "code": USECASE_INPUT_VALIDATION_ERROR,
        "detail": exc.detail,
    }


def test_exception_handler_with_value_error():
    exc = ValueError("test")
    resp = exception_handler(None, exc)

    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert json.loads(resp.body.decode("utf-8")) == {
        "message": "test",
        "code": UNKNOWN_ERROR,
        "detail": str(exc),
    }
