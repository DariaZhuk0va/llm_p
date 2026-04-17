# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    Схема запроса к LLM
    """
    prompt: str = Field(
                    ...,
                    description="Основной текст запроса пользователя"
                    )
    system: Optional[str] = Field(
                    None,
                    description="Системная инструкция (необязательно)"
                    )
    max_history: Optional[int] = Field(
                    10,
                    ge=1,
                    description="Количество последних сообщений из истории (по умолчанию 10)"
                    )
    temperature: Optional[float] = Field(
                                        0.7,
                                        ge=0.0,
                                        le=2.0,
                                        description="Креативность модели (0.0 — детерминированно, 2.0 — максимально случайно)"
                                        )

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "Расскажи о FastAPI",
                "system": "Ты полезный ассистент",
                "max_history": 5,
                "temperature": 0.8
            }
        }
    }


class ChatResponse(BaseModel):
    """
    Схема ответа от LLM
    """
    answer: str = Field(
                    ...,
                    description="Ответ модели"
                    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "FastAPI — это современный веб-фреймворк для Python..."
            }
        }
    }