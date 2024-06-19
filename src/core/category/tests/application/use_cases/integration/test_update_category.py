from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        expected_name = "Films"
        expected_description = "New Films description"

        category = Category(
            name="Film",
            description="Film description",
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.create(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name=expected_name,
            description=expected_description,
        )
        use_case.execute(request)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == expected_name
        assert updated_category.description == expected_description
