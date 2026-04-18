from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage
from app.schemas.chat import MessageRole


class ChatMessageRepository:
    """
    Репозиторий для доступа к данным сообщений чата
    """
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def add_message(self, user_id: int, role: MessageRole, content: str) -> ChatMessage:
        """
        Добавить сообщение в историю чата.
        
        user_id: ID пользователя
        role: Роль отправителя сообщения в чате 
        content: Текст сообщения

        return: Созданный объект ChatMessage
        """
        async with self._session.begin():
            message = ChatMessage(user_id=user_id, role=role, content=content)
            self._session.add(message)
            await self._session.flush()
            await self._session.refresh(message)
        return message
    
    async def get_last_n(self, user_id: int, n: int) -> List[ChatMessage]:
        """
        Получить последние N сообщений пользователя
        в хронологическом порядке (от старых к новым).
        
        :param user_id: ID пользователя
        :param n: Количество сообщений
        :return: Список сообщений (самые новые в конце)
        """
        
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(n)
        )
        result = await self._session.execute(stmt)
        messages = result.scalars().all()
        
        return list(reversed(messages))
    
    async def delete_all_for_user(self, user_id: int) -> None:
        """
        Удалить все сообщения пользователя
        """
        async with self._session.begin():
            stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
            await self._session.execute(stmt)