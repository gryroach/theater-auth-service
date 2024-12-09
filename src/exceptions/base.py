class CustomException(Exception):
    """Базовый класс для всех кастомных исключений."""

    def __init__(self, message: str):
        self.message = message
