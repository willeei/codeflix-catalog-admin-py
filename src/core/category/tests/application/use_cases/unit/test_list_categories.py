from unittest.mock import create_autospec

from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, \
    ListCategoryResponse, CategoryOutput
from src.core.category.domain.category import Category


class TestListCategories:
    def test_when_no_categories_in_repository_then_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.find_all.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_in_repository_then_return_list(self):
        category_films = Category(
            name="Films",
            description="Films description",
            is_active=True,
        )
        category_series = Category(
            name="Series",
            description="Series description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.find_all.return_value = [category_films, category_series]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_films.id,
                    name=category_films.name,
                    description=category_films.description,
                    is_active=category_films.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                )
            ]
        )
