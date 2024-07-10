from rest_framework.test import APITestCase


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            [
                {
                    "id": "1683f484-a7aa-4728-8bac-16c7c78ec46f",
                    "name": "Category 1",
                    "description": "Category 1 description",
                    "is_active": True
                },
                {
                    "id": "f228060a-c292-4ab0-81a2-9011d62acdd7",
                    "name": "Category 2",
                    "description": "Category 2 description",
                    "is_active": True
                }
            ]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
