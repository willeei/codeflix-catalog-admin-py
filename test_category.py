import unittest

from category import Category


class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_or_equal_than_255_characters(self):
        with self.assertRaisesRegex(ValueError, "name must have less or equal than 255 characters"):
            Category("a" * 256)


if __name__ == "__main__":
    unittest.main()
