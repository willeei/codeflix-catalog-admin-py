from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest:
    pass


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.find_all()

        return ListCategoryResponse(
            # list comprehension // dict comprehension
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                ) for category in categories
            ]
        )
