from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] = None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category):
        self.categories.append(category)

    def get_by_id(self, category_id: UUID) -> Category | None:
        return next(
            (category for category in self.categories
                if category.id == category_id),
            None,
        )
        # for category in self.categories:
        #     if category.id == category_id:
        #         return category
        # return None

    def delete(self, category_id: UUID) -> None:
        category = self.get_by_id(category_id)
        if category:
            self.categories.remove(category)

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)

    def list(self) -> list[Category]:
        return [category for category in self.categories]
