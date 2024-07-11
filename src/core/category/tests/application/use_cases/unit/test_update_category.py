import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound, InvalidCategory)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory, UpdateCategoryRequest)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestUpdateCategory:
    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name="Filme",
            description="Categoria de filme",
        )

    @pytest.fixture
    def mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository, instance=True)
        repository.get_by_id.return_value = category
        return repository

    def test_update_category_name(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ):
        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, name="Filmes",))

        assert category.name == "Filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ):
        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id, description="Categoria de Filmes",
        ))

        assert category.description == "Categoria de Filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_activate_category(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        category.deactivate()

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(id=category.id, is_active=True))

        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)

    def test_deactivate_category(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        category.activate()

        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        ))

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_update_categoru_name_and_description(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        use_case = UpdateCategory(repository=mock_repository)
        use_case.execute(UpdateCategoryRequest(
            id=category.id,
            name="Filmes",
            description="Categoria de Filmes",
        ))

        assert category.name == "Filmes"
        assert category.description == "Categoria de Filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_when_category_not_found_then_raise_exception(self):
        category_id = uuid.uuid4()
        expected_error_message = f"Category with id {category_id} not found"

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert exc.type is CategoryNotFound
        assert str(exc.value) == expected_error_message

    def test_when_category_call_update_with_long_name_should_raise_exception(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ) -> None:
        expected_error_message = "name cannot be longer than 255 characters"

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="a" * 256,
        )

        with pytest.raises(InvalidCategory) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert exc.type is InvalidCategory
        assert str(exc.value) == expected_error_message
