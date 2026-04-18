from typing import List, Dict, Optional

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import MessageRole
from app.core.errors import ExternalServiceError


class ChatUseCase:
    """
    Бизнес-логика общения с LLM
    """

    def __init__(
        self,
        chat_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ):
        self.chat_repo = chat_repo
        self.openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: Optional[str] = None,
        max_history: int = 10,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Обработка запроса пользователя к LLM.

        user_id: ID пользователя
        prompt: Текущий запрос пользователя
        system: Системная инструкция (опционально)
        max_history: Сколько последних сообщений взять из истории
        temperature: Креативность модели
        model: Модель (опционально, иначе дефолтная)
        
        return: Ответ модели
        """

        messages: List[Dict[str, str]] = []


        if system:
            messages.append({"role": "system", "content": system})

        history = await self.chat_repo.get_last_n(user_id, max_history)

        for msg in history:
            messages.append({
                "role": msg.role.value, 
                "content": msg.content,
            })


        messages.append({"role": MessageRole.USER.value, "content": prompt})

        await self.chat_repo.add_message(
            user_id=user_id,
            role=MessageRole.USER,
            content=prompt,
        )

        try:
            answer = await self.openrouter_client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
            )
        except ExternalServiceError:
            raise

        await self.chat_repo.add_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=answer,
        )

        return answer

    async def clear_history(self, user_id: int) -> None:
        """
        Удалить всю историю чата пользователя

        user_id: ID пользователя
        """
        await self.chat_repo.delete_all_for_user(user_id)