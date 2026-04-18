from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """
    Отправить сообщение LLM и получить ответ с учётом истории
    """
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history or 10,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM service error: {str(e)}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/history", response_model=List[dict])
async def get_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """
    Получить всю историю сообщений пользователя
    """
    try:
        history = await chat_usecase.get_history(user_id)
        return history
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """
    Очистить всю историю сообщений пользователя
    """
    try:
        await chat_usecase.clear_history(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )