from pkg.exceptions import UNKNOWN_ERROR, TranslatableException
from pkg.i18n import new_message


def translate(*args, **kwargs):
    return "test"


def test_translatableexception_methods():
    value_error = ValueError("test")
    try:
        raise TranslatableException(
            value_error, new_message("test1", "test2"), _translate_func=translate
        )
    except TranslatableException as e:
        assert e.code == UNKNOWN_ERROR
        assert e.unwrap() == value_error
        assert e.display_message == "test"
        assert str(e) == "test"
        assert e.__repr__() == "test"

    try:
        raise TranslatableException(value_error, new_message("test1", "test2"))
    except TranslatableException as e:
        assert e.code == UNKNOWN_ERROR
        assert e.unwrap() == value_error
        assert e.display_message == "test1"
        assert str(e) == "test"
        assert e.__repr__() == "test1"

    try:
        raise TranslatableException(value_error, None)
    except TranslatableException as e:
        assert e.code == UNKNOWN_ERROR
        assert e.unwrap() == value_error
        assert e.display_message == "test"
        assert str(e) == "test"
        assert e.__repr__() == "test"
