from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    InvalidCategory
)
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
        """
        - Busca categoria por ID
        - Atualiza categoria com os valores passados
        - Ativar/desativar a categoria
        - Salvar essa categoria
        """
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        try:
            if request.is_active is True:
                category.activate()

            if request.is_active is False:
                category.deactivate()

            current_name = category.name
            current_description = category.description

            if request.name is not None:
                current_name = request.name

            if request.description is not None:
                current_description = request.description

            category.update(name=current_name, description=current_description)
        except ValueError as err:
            raise InvalidCategory(err) from err

        self.repository.update(category)
