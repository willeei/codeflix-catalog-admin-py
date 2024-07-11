from pytest import mark

from core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryModel
from django_project.category_app.repository import DjangoORMCategoryRepository


@mark.django_db
class TestCreate:
    def test_create_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active
