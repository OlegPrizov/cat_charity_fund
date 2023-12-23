from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User
from app.schemas.user import UserCreate

LACK_OF_SYMBOLS_MESSAGE = 'Password should be at least 3 characters'
EMAIL_IN_PASSWORD_MESSAGE = 'Пароль не должен содержать эл. почту!'
EXISTING_EMAIL_MESSAGE = 'Пользователь c почтой {} уже зарегистрирован!'
JWT_LIFETIME_IN_SECONDS = 3600


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy():
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=JWT_LIFETIME_IN_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ):
        if len(password) < 3:
            raise InvalidPasswordException(LACK_OF_SYMBOLS_MESSAGE)
        if user.email in password:
            raise InvalidPasswordException(EMAIL_IN_PASSWORD_MESSAGE)

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ):
        print(EXISTING_EMAIL_MESSAGE.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
