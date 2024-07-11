from src.core.category.domain.category import Category

category_1 = Category(name="Movie", description="Movie description")
category_2 = Category(name="Documentary", description="Documentary description")
category_3 = Category(name="Movie", description="Movie description")

print(category_1 == category_2)  # False
print(category_1 == category_3)  # True

# category_1.__eq__(category_2)  # False
