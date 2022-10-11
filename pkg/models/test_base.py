from pkg.models.base import Base


def test_base_tablename():
    class TestTableName(Base):
        pass

    assert TestTableName.__tablename__ == "testtablename"
