from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, category_id) -> Category | None:
        pass
