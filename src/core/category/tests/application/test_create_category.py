from uuid import UUID

from src.core.category.application.create_category import create_category


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        category_id = create_category(
            name="Films", description="Films about action", is_active=True
        )

        assert category_id is not None
        assert isinstance(category_id, UUID)
