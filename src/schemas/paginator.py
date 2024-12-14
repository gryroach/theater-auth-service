from pydantic import BaseModel


class Paginator(BaseModel):
    page: int = 1
    size: int = 10

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size

    def to_response(self, data: list, has_next: bool) -> dict:
        """Формат ответа с метаданными пагинации."""
        return {
            "data": data,
            "pagination": {
                "page": self.page,
                "size": self.size,
                "has_next": has_next,
            },
        }
