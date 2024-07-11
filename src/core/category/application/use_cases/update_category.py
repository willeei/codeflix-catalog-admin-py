from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound, InvalidCategoryData)
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


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

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name

        if request.description is not None:
            current_description = request.description

        try:
            category.update(name=current_name, description=current_description)
        except ValueError as err:
            raise InvalidCategoryData(err) from err

        if request.is_active is not None:
            if request.is_active:
                category.activate()
            else:
                category.deactivate()

        self.repository.update(category)
