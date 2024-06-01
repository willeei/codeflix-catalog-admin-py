import uuid

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Films",
            description="Category of films",
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetByIdInMemoryCategoryRepository:
    def test_can_get_category_by_id(self):
        category = Category(
            name="Films",
            description="Category of films",
        )
        repository = InMemoryCategoryRepository(categories=[category])

        result = repository.get_by_id(category.id)

        assert result == category

    def test_when_category_does_not_exist_then_return_none(self):
        repository = InMemoryCategoryRepository()

        result = repository.get_by_id(uuid.uuid4())

        assert result is None
        assert len(repository.categories) == 0

class TestDeleteInMemoryCategoryRepository:
    def test_can_delete_category(self):
        category = Category(
            name="Films",
            description="Category of films",
        )
        repository = InMemoryCategoryRepository(categories=[category])

        repository.delete(category.id)

        assert len(repository.categories) == 0

    def test_when_category_does_not_exist_then_do_nothing(self):
        repository = InMemoryCategoryRepository()

        repository.delete(uuid.uuid4())

        assert len(repository.categories) == 0