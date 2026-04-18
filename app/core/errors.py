from typing import Optional


class AppError(Exception):
    """
    Базовое исключение приложения
    """
    pass


class ConflictError(AppError):
    """
    Ресурс уже существует (например, email уже зарегистрирован)
    """
    pass


class UnauthorizedError(AppError):
    """
    Неверные учетные данные или отсутствует аутентификация
    """
    pass


class ForbiddenError(AppError):
    """
    Нет прав доступа к ресурсу
    """
    pass


class NotFoundError(AppError):
    """
    Объект не найден в базе данных
    """
    def __init__(
            self,
            message: str = "Object not found",
            entity_id: Optional[str] = None
            ):
        self.entity_id = entity_id
        super().__init__(message)


class ExternalServiceError(AppError):
    """
    Ошибка при вызове внешнего сервиса (например, OpenRouter)
    """
    def __init__(
            self,
            service_name: str,
            original_error: Optional[Exception] = None
            ):
        self.service_name = service_name
        self.original_error = original_error
        message = f"External service '{service_name}' error"
        if original_error:
            message += f": {str(original_error)}"
        super().__init__(message)