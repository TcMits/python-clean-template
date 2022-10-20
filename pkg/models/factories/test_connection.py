from pkg.models.factories import connection


def test_connection_configure_engine():
    class FakeEngine:
        pass

    with connection.configure_engine(FakeEngine()):
        try:
            with connection.configure_engine(FakeEngine()):
                pass
        except Exception as e:
            assert isinstance(e, ValueError)
        else:
            assert 1 == 0


def test_connection_get_session():
    class FakeEngine:
        pass

    try:
        connection.get_session()
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert 1 == 0

    with connection.configure_engine(FakeEngine()):
        assert connection.get_session() is not None
