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


@mark.django_db
class TestGetByID:
    def test_get_category_by_id(self):
        category = Category(
            name="Movie",
            description="Movie description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category)
        assert CategoryModel.objects.count() == 1

        actual_category = repository.get_by_id(category.id)
        assert actual_category.id == category.id
        assert actual_category.name == category.name
        assert actual_category.description == category.description
        assert actual_category.is_active == category.is_active


@mark.django_db
class TestDelete:
    def test_delete_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category)
        assert CategoryModel.objects.count() == 1

        repository.delete(category.id)
        assert CategoryModel.objects.count() == 0


@mark.django_db
class TestFindAll:
    def test_find_all_categories(self):
        category_movie = Category(
            name="Movie",
            description="Movie description"
        )
        category_music = Category(
            name="Music",
            description="Music description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category_movie)
        repository.create(category_music)
        assert CategoryModel.objects.count() == 2

        categories = repository.find_all()
        assert len(categories) == 2

        actual_category = categories[0]
        assert actual_category.id == category_movie.id
        assert actual_category.name == category_movie.name
        assert actual_category.description == category_movie.description
        assert actual_category.is_active == category_movie.is_active

        actual_category = categories[1]
        assert actual_category.id == category_music.id
        assert actual_category.name == category_music.name
        assert actual_category.description == category_music.description
        assert actual_category.is_active == category_music.is_active


@mark.django_db
class TestUpdate:
    def test_update_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description"
        )
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category)
        assert CategoryModel.objects.count() == 1

        assert category.id is not None
        assert category.name == "Movie"
        assert category.description == "Movie description"
        assert category.is_active is True

        actual_category = repository.get_by_id(category.id)

        actual_category.name = "Music"
        actual_category.description = "Music description"
        actual_category.is_active = False

        repository.update(actual_category)

        category_db = CategoryModel.objects.get()
        assert category_db.id == actual_category.id
        assert category_db.name == actual_category.name
        assert category_db.description == actual_category.description
        assert category_db.is_active == actual_category.is_active
