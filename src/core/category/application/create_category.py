from uuid import UUID

from src.core.category.domain.category import Category


def create_category(name: str, description: str, is_active: bool = True) -> UUID:
    category = Category(name=name, description=description, is_active=is_active)

    return category.id
