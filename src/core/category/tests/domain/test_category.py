import uuid
from dataclasses import dataclass
from uuid import UUID

import pytest

from src.core.category.domain.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_or_equal_than_255_characters(self):
        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
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
            id=category_id, name="Films", description="Movies", is_active=False
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
        assert repr(category) == f"<Category Films ({category.id})>"

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Films", description="Films about action")

        category.update(name="Movies", description="Action Movies")

        assert category.name == "Movies"
        assert category.description == "Action Movies"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="Films", description="Films about action")

        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            category.update(name="a" * 256, description="Action Movies")

    def test_update_category_with_empty_name_raises_exception(self):
        category = Category(name="Films", description="Films about action")

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update(name="", description="Action Movies")


class TestActivateAndDeactivateCategory:
    def test_activate_an_inactive_category(self):
        category = Category(
            name="Films", description="Films about action", is_active=False
        )

        category.activate()

        assert category.is_active is True

    def test_activete_an_active_category(self):
        category = Category(
            name="Films", description="Films about action", is_active=True
        )

        category.activate()

        assert category.is_active is True

    def test_deactivate_an_active_category(self):
        category = Category(
            name="Films", description="Films about action", is_active=True
        )

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_an_inactive_category(self):
        category = Category(
            name="Films", description="Films about action", is_active=False
        )

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        category_id = uuid.uuid4()
        category1 = Category(id=category_id, name="Films")
        category2 = Category(id=category_id, name="Films")

        assert category1 == category2

    def test_categories_with_different_id_are_not_equal(self):
        category1 = Category(name="Films")
        category2 = Category(name="Films")

        assert category1 != category2

    def test_equality_diffetent_classes(self):
        @dataclass
        class Dummy:
            id: uuid.UUID = uuid.uuid4()

        common_id = uuid.uuid4()
        category = Category(name="Films", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
