from gettext import NullTranslations
from unittest.mock import MagicMock

from pkg import gettext


def test_add_translation():
    null_trans = NullTranslations()
    gettext.add_translation("vi", null_trans)
    assert gettext._default == null_trans
    gettext.clear_translations()


def test_activate():
    null_trans = NullTranslations()
    null_trans_2 = NullTranslations()

    gettext.add_translation("vi", null_trans)
    gettext.add_translation("en_US", null_trans_2)
    gettext.activate("en_US")

    assert gettext.get_active_translation() == null_trans_2
    gettext.clear_translations()


def test_deactivate():
    null_trans = NullTranslations()
    null_trans_2 = NullTranslations()

    gettext.add_translation("vi", null_trans)
    gettext.add_translation("en_US", null_trans_2)
    gettext.activate("en_US")
    gettext.deactivate()

    assert gettext.get_active_translation() == null_trans
    gettext.clear_translations()


def test_gettext():
    null_trans = NullTranslations()
    null_trans.gettext = MagicMock(return_value="translated str")
    gettext.add_translation("vi", null_trans)

    gettext.gettext("singular")

    null_trans.gettext.assert_called_once_with("singular")
    gettext.clear_translations()


def test_ngettext():
    null_trans = NullTranslations()
    null_trans.ngettext = MagicMock(return_value="translated str")
    gettext.add_translation("vi", null_trans)

    gettext.ngettext("singular", "plural", 2)

    null_trans.ngettext.assert_called_once_with("singular", "plural", 2)
    gettext.clear_translations()
