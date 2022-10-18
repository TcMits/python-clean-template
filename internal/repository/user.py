from internal.repository.read import SimpleGetRepository
from pkg.models.user import User


class UserGetLoginRepository(SimpleGetRepository[User]):
    _model_class = User
