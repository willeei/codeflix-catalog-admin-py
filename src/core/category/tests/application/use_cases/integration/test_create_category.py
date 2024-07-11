from uuid import UUID

from src.core.category.application.use_cases.create_category import (
    CreateCategory, CreateCategoryRequest)
from src.core.category.infra.in_memory_category_repository import \
    InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):

        # SQLAlchmy / # DjangoORMRepository
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)

        # expects
        expected_name = "Filme"
        expected_description = "Categoria para filmes"
        expected_is_active = True

        request = CreateCategoryRequest(
            name=expected_name,
            description=expected_description,
            is_active=expected_is_active,  # default
        )

        response = use_case.execute(request)

        assert response is not None
        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == expected_name
        assert persisted_category.description == expected_description
        assert persisted_category.is_active is expected_is_active

    def test_create_inactive_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)

        # expects
        expected_name = "Filme"
        expected_description = "Categoria para filmes"
        expected_is_active = False

        request = CreateCategoryRequest(
            name=expected_name,
            description=expected_description,
            is_active=expected_is_active,
        )

        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == expected_name
        assert persisted_category.description == expected_description
        assert persisted_category.is_active is expected_is_active
