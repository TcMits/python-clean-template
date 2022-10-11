from pkg.dao.base import DAOBase
from pkg.models.user import User


class UserDAO(DAOBase[User]):
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
