from typing import Annotated

from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UnauthorizedError
from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """
    Предоставляет репозиторий пользователей
    """
    return UserRepository(session)


def get_chat_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> ChatMessageRepository:
    """
    Предоставляет репозиторий сообщений чата
    """
    return ChatMessageRepository(session)

def get_openrouter_client() -> OpenRouterClient:
    """
    Предоставляет клиент OpenRouter
    """
    return OpenRouterClient()

def get_auth_usecase(user_repo: Annotated[UserRepository, Depends(get_user_repo)],) -> AuthUseCase:
    """
    Предоставляет usecase аутентификации
    """
    return AuthUseCase(user_repo)


def get_chat_usecase(
    chat_repo: Annotated[ChatMessageRepository, Depends(get_chat_repo)],
    openrouter_client: Annotated[OpenRouterClient, Depends(get_openrouter_client)],
) -> ChatUseCase:
    """
    Предоставляет usecase чата
    """
    return ChatUseCase(chat_repo, openrouter_client)


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """
    Извлекает user_id из JWT токена.
    
    token: JWT access token из заголовка Authorization
    
    return: user_id (из поля sub)
    """
    try:
        payload = decode_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise UnauthorizedError("Token does not contain sub claim")
        return int(user_id_str)
    except (jwt.InvalidTokenError, ValueError, UnauthorizedError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )