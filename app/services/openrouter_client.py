import httpx
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """
    Клиент для взаимодействия с API OpenRouter
    """

    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.referer = settings.OPENROUTER_REFERER
        self.title = settings.OPENROUTER_TITLE
        self.default_model = settings.OPENROUTER_DEFAULT_MODEL
        self.timeout = settings.OPENROUTER_TIMEOUT

    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000", 
            "X-Title": "My LLM App",                 
        }
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.title:
            headers["X-Title"] = self.title
        return headers

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Отправить запрос к OpenRouter и получить ответ модели
        """
        if not messages:
            raise ExternalServiceError(
                service_name="OpenRouter",
                original_error=Exception("Messages list cannot be empty")
            )

        url = f"{self.base_url}/chat/completions"
        headers = self._build_headers()

        payload: Dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(
                    service_name="OpenRouter",
                    original_error=e
                    )
            except httpx.RequestError as e:
                raise ExternalServiceError(
                    service_name="OpenRouter",
                    original_error=e
                    )
            except Exception as e:
                raise ExternalServiceError(
                    service_name="OpenRouter",
                    original_error=e
                    )

        try:
            choices = data.get("choices", [])
            if not choices:
                raise ExternalServiceError(
                    service_name="OpenRouter",
                    original_error=Exception("No choices in response")
                )
            answer = choices[0].get("message", {}).get("content", "")
            return answer
        except (KeyError, IndexError, TypeError) as e:
            raise ExternalServiceError(
                service_name="OpenRouter",
                original_error=e
                )