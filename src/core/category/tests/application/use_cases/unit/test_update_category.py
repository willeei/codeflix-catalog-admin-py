import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Film",
            description="Film description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Films",
        )
        use_case.execute(request)

        assert category.name == "Films"
        assert category.description == "Film description"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        expected_description = "Film description updated"
        category = Category(
            name="Film",
            description="Film description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description=expected_description,
        )
        use_case.execute(request)

        assert category.name == "Film"
        assert category.description == expected_description
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            name="Film",
            description="Film description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        )
        use_case.execute(request)

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name="Film",
            description="Film description",
            is_active=False,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True,
        )
        use_case.execute(request)

        assert category.is_active is not False
        mock_repository.update.assert_called_once_with(category)

    def test_raise_exception_when_category_not_found(self):
        category_id = uuid.uuid4()
        expected_error_message = f"Category with id {category_id} not found"

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category_id
        )

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert exc_info.type is CategoryNotFound
        assert str(exc_info.value) == expected_error_message

    def test_raise_exception_when_an_invalid_category_is_called(self):
        expected_error_message = "name cannot be longer than 255 characters"

        category = Category(
            name="Film",
            description="Description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="a" * 256,
        )

        with pytest.raises(InvalidCategoryData, match=expected_error_message) as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == expected_error_message
