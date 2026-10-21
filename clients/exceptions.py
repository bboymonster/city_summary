class AppError(Exception):
    """Базовое исключение приложения."""
    pass

class EntityNotFoundError(AppError):
    """Город или валюта не найдены (код выхода 3)."""
    pass

class ServiceUnavailableError(AppError):
    """Внешний сервис недоступен после всех попыток (код выхода 4)."""
    pass