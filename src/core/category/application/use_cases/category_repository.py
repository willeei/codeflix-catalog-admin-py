from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, category_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category):
        raise NotImplementedError
