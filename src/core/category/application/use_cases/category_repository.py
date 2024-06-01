from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        raise NotImplementedError

    def delete(self, category_id: UUID) -> None:
        raise NotImplementedError
