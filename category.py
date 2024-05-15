import uuid


class Category:
    def __init__(
            self,
            name,
            id="",
            description="",
            is_active=True,
    ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

    def __str__(self):
        return f"{self.name} - {self.description} - {self.is_active}"

    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"
