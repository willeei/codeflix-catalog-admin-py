import pytest
import uuid
from uuid import UUID

from category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_or_equal_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less or equal than 255 characters"):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Films")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Films")
        assert category.name == "Films"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Films")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Films",
            description="Movies",
            is_active=False
        )
        assert category.id == category_id
        assert category.name == "Films"
        assert category.description == "Movies"
        assert category.is_active is False

    def test_category_str_method(self):
        category = Category(name="Films", description="Movies", is_active=False)
        assert str(category) == "Films - Movies - False"

    def test_category_repr_method(self):
        category = Category(name="Films", description="Movies", is_active=False)
        assert repr(category) == "<Category Films ({})>".format(category.id)
