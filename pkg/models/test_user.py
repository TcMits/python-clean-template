from sqlalchemy import inspect

from pkg.models.user import User


def test_count_user_fields():
    insp = inspect(User)

    assert len(list(insp.columns)) == 10
