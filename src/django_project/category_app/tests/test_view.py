import uuid
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import (
    DjangoORMCategoryRepository,
)


@pytest.fixture(name="category_movie")
def movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture(name="category_documentary")
def documentary() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture(name="category_repository")
def repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)
        category_repository.save(category=category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/invalid_id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)
        category_repository.save(category=category_documentary)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_not_exists(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",  # Name não pode ser vazio
                "description": "Movie description",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self, category_repository: DjangoORMCategoryRepository
    ) -> None:
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_category_id = uuid.UUID(response.data["id"])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie",
            description="Movie description",
        )

        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Movie",
                description="Movie description",
            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/123456/"  # UUID inválido
        response = APIClient().put(
            url,
            data={
                "name": "",  # Name não pode ser vazio
                "description": "Movie description",
                # is_active is missing
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."],
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name="Documentary",
            description="Documentary description",
            is_active=True,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_category_does_not_exists_then_return_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/123456/"  # UUID inválido
        response = APIClient().patch(
            url,
            data={
                "name": "",  # Name não pode ser vazio
                "description": "Movie description",
                # is_active is missing
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name="Documentary",
            description="Documentary description",
            is_active=True,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_update_only_name_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Documentary",
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name="Documentary",
            description=category_movie.description,
            is_active=category_movie.is_active,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_update_only_description_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "description": "Documentary description",
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description="Documentary description",
            is_active=category_movie.is_active,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_update_only_is_active_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=False,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_update_with_empty_payload_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={},
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=category_movie.is_active,
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.id == expected_category.id
        assert updated_category.name == expected_category.name
        assert updated_category.description == expected_category.description
        assert updated_category.is_active == expected_category.is_active

    def test_when_category_does_not_exists_then_return_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_then_return_400(self) -> None:
        url = "/api/categories/123456/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_does_not_exists_then_return_404(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_exists_then_delete_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category=category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_movie.id) is None
        assert category_repository.list() == []
