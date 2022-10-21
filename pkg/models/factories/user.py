import factory

from pkg.models.factories import connection
from pkg.models.user import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = connection.get_factory_session()

    username = factory.Sequence(lambda n: "username%d" % n)
    password = None
    email = factory.Sequence(lambda n: "email%d@gmail.com" % n)
    first_name = factory.Sequence(lambda n: "first name %d" % n)
    last_name = factory.Sequence(lambda n: "last name %d" % n)
    is_staff = True
    is_superuser = False
    is_active = True
