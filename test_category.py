import unittest
import uuid
from uuid import UUID

from category import Category


class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_or_equal_than_255_characters(self):
        with self.assertRaisesRegex(ValueError, "name must have less or equal than 255 characters"):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Films")
        self.assertEqual(type(category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Films")
        self.assertEqual(category.name, "Films")
        self.assertEqual(category.description, "")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Films")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Films",
            description="Movies",
            is_active=False
        )
        self.assertEqual(category.id, category_id)
        self.assertEqual(category.name, "Films")
        self.assertEqual(category.description, "Movies")
        self.assertEqual(category.is_active, False)


if __name__ == "__main__":
    unittest.main()
