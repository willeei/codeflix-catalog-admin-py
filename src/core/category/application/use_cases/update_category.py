from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.category_repository import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str


@dataclass
class UpdateCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        category.name = request.name
        self.repository.update(category)
