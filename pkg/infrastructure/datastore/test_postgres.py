from pkg.infrastructure.datastore.postgres import get_engine


def test_get_engine(mocker):
    create_engine_mock = mocker.patch(
        "pkg.infrastructure.datastore.postgres.create_engine"
    )
    database_url = "test.com"
    pool_size = 2
    get_engine(database_url, pool_size)
    create_engine_mock.assert_called_once_with(
        url=database_url, pool_size=pool_size, pool_pre_ping=True
    )
