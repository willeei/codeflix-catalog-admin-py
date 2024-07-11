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
        category_film = Category(
            id=uuid.uuid4(),
            name="Film",
            description="Film description",
            is_active=True,
        )
        category_series = Category(
            id=uuid.uuid4(),
            name="Series",
            description="Series description",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[category_film, category_series]
        )

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_film.id)
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_film.id,
            name="Film",
            description="Film description",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_film = Category(
            name="Film",
            description="Film description",
            is_active=True,
        )
        category_series = Category(
            name="Series",
            description="Series description",
            is_active=True,
        )

        repository = InMemoryCategoryRepository(
            categories=[category_film, category_series]
        )

        use_case = GetCategory(repository=repository)
        not_exist_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_exist_id)

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
