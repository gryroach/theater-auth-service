class InvalidCredentialsError(Exception):
    """Ошибка при некорректных учетных данных."""

    def __init__(self, message: str = "Invalid login or password"):
        self.message = message
        super().__init__(self.message)
