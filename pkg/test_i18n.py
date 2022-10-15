from pkg.i18n import new_message


def test_new_message():
    msg = new_message("test1", "test2")

    assert msg.singular == "test1"
    assert msg.plural == "test2"
