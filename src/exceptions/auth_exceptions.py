from exceptions.base import CustomException


class InvalidCredentialsError(Exception):
    """Ошибка при некорректных учетных данных."""

    def __init__(self, message: str = "Invalid login or password"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(CustomException):
    """Ошибка истечения срока действия токена."""

    pass


class InvalidTokenError(CustomException):
    """Ошибка недействительного токена."""

    pass


class InvalidSessionError(CustomException):
    """Ошибка недействительной или истекшей сессии."""

    pass


class UserNotFoundError(CustomException):
    """Ошибка, если пользователь не найден."""

    pass
