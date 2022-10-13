from internal.usecase.base import LoginUseCase as BaseLoginUseCase
from pkg.models.user import User


class LoginUseCase(BaseLoginUseCase[User]):
    pass
