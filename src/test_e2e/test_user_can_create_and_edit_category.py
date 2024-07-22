import pytest

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        # Verifica se a lista está vazia
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

        # Cria uma nova categoria
        create_response = api_client.post(
            "/api/categories/",
            data={"name": "Movie", "description": "Movie description"},
            format="json",
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        # Verifica se a categoria foi criada
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ],
        }

        # Edita categoria criada
        update_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "New Movie",
                "description": "New description",
                "is_active": False,
            },
        )
        assert update_response.status_code == 204

        # Verifica se a categoria foi editada
        retrieve_response = api_client.get(
            f"/api/categories/{created_category_id}/",
            format="json"
        )
        expected_data = {
            "data": {
                "id": str(created_category_id),
                "name": "New Movie",
                "description": "New description",
                "is_active": False,
            }
        }
        assert retrieve_response.data == expected_data
