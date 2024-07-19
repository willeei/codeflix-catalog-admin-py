import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import \
    InMemoryCategoryRepository


class TestCreateCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            id=uuid.uuid4(),
            name="Filmes",
            description="Categoria para filmes",
            is_active=True,
        )
        category_series = Category(
            id=uuid.uuid4(),
            name="Series",
            description="Categoria para series",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name="Filmes",
            description="Categoria para filmes",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_not_found(self):
        category_filme = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True,
        )
        category_series = Category(
            name="Series",
            description="Categoria para series",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )

        use_case = GetCategory(repository=repository)
        not_exist_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_exist_id)

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
