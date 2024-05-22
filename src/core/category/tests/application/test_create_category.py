from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.create_category import InvalidCategoryData, create_category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(InMemoryCategoryRepository)
        category_id = create_category(
            repository=mock_repository,
            name="Films",
            description="Films about action",
            is_active=True
        )

        assert category_id is not None
        assert isinstance(category_id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        mock_repository = MagicMock(InMemoryCategoryRepository)
        with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
            create_category(
                repository=mock_repository,
                name="",
                description=""
            )
        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
