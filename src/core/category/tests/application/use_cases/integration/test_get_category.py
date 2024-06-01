from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_get_category_by_id(self):
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
        request = GetCategoryRequest(
            id=category_film.id,
        )

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_film.id,
            name="Film",
            description="Film description",
            is_active=True,
        )
