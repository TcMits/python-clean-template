import os

from config import get_settings


def test_get_settings(mocker):
    database_url = "postgres://user:pass@localhost:5432/foobar"
    mocker.patch.dict(os.environ, {"DATABASE_URL": database_url})

    settings_1 = get_settings()
    assert settings_1.DATABASE_URL == database_url
    assert settings_1.POOL_SIZE == 100
    assert settings_1.GUNICORN_BIND_ADDR == "0.0.0.0:8000"
    assert settings_1.GUNICORN_WORKERS == 1
    assert settings_1.GUNICORN_THREADS == 2
    assert settings_1.GUNICORN_RELOAD == False

    settings_1.POOL_SIZE = 50
    settings_2 = get_settings()
    assert settings_2.POOL_SIZE == 100
