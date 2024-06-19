import uuid

from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
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

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_film.id)

        assert repository.get_by_id(category_film.id) is not None
        assert use_case.execute(request) is None

        assert repository.get_by_id(category_film.id) is None
