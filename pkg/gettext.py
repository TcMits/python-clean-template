from gettext import NullTranslations
from typing import Optional

from asgiref.local import Local

__translations = {}
_active = Local()
_default = None


def clear_translations() -> None:
    global __translations
    global _default
    __translations = {}
    _default = None
    deactivate()


def add_translation(language: str, translation: NullTranslations) -> None:
    global __translations
    global _default
    __translations.update({language: translation})
    if _default is None:
        _default = translation


def get_active_translation() -> Optional[NullTranslations]:
    return getattr(_active, "value", _default)


def activate(language: str) -> None:
    """
    Fetch the translation object for a given language and install it as the
    current translation object for the current thread.
    """
    global __translations
    if not language:
        return
    _active.value = __translations.get(language, _default)


def deactivate() -> None:
    """
    Uninstall the active translation object so that further _() calls resolve
    to the default translation object.
    """
    if hasattr(_active, "value"):
        del _active.value


def gettext(message: str) -> str:
    """
    Translate the 'message' string. It uses the current thread to find the
    translation object to use. If no current translation is activated, the
    message will be run through the default translation object.
    """
    global _default

    eol_message = message.replace("\r\n", "\n").replace("\r", "\n")
    result = message

    if eol_message:
        translation_object = get_active_translation()
        if translation_object:
            result = translation_object.gettext(eol_message)

    return result


def ngettext(singular: str, plural: str, number: int) -> str:
    result = singular if number == 1 else plural
    translation_object = get_active_translation()
    if translation_object:
        result = translation_object.ngettext(singular, plural, number)
    return result
