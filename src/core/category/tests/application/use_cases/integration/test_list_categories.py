from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, \
    ListCategoryResponse, CategoryOutput
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategories:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
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
        repository = InMemoryCategoryRepository()
        repository.create(category_films)
        repository.create(category_series)

        use_case = ListCategory(repository)
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
