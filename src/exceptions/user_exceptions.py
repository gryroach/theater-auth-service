from exceptions.base import CustomException


class UserError(Exception):
    """Базовое исключение для всех ошибок, связанных с пользователями."""

    pass


class UserAlreadyExistsError(UserError):
    """Ошибка, если пользователь уже существует"""

    pass


class UserNotFoundError(UserError):
    """Ошибка, если пользователь не найден."""

    pass

  
class UserDoesNotExistsError(UserError):
    """Ошибка, если пользователь не существует."""
    
    pass
