import pytest
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import \
    InMemoryCategoryRepository


class TestListCategories:
    @pytest.fixture
    def category_movies(self) -> Category:
        return Category(
            name="Movies",
            description="Movies description"
        )

    @pytest.fixture
    def category_series(self) -> Category:
        return Category(
            name="Series",
            description="Series description"
        )

    def test_when_no_categories_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=empty_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_exist_then_return_mapped_list(
        self,
        category_movies: Category,
        category_series: Category,
    ) -> None:
        repository = InMemoryCategoryRepository()
        repository.save(category=category_movies)
        repository.save(category=category_series)

        use_case = ListCategory(repository=repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_movies.id,
                    name=category_movies.name,
                    description=category_movies.description,
                    is_active=category_movies.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ]
        )
