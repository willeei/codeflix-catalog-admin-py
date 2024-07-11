import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestGetCategory:
    def test_return_found_category(self):
        expected_name = "Filmes"
        expected_description = "Categoria de filmes"
        expected_id = uuid.uuid4()
        expected_is_active = True

        mock_category = Category(
            id=expected_id,
            name=expected_name,
            description=expected_description,
            is_active=expected_is_active,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=mock_category.id)
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=expected_id,
            name=expected_name,
            description=expected_description,
            is_active=expected_is_active
        )

    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
