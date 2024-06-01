from unittest.mock import create_autospec

from src.core.category.application.use_cases.category_repository import CategoryRepository
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
        pass

    def test_can_deactivate_category(self):
        pass
