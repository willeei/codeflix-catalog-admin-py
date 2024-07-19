from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest
)
from src.django_project.category_app.repository import \
    DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def list(self, _: Request) -> Response:
        _input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=_input)
        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active
            } for category in output.data
        ]

        return Response(status=HTTP_200_OK, data=categories)

    def retrieve(self, _: Request, pk=None) -> Response:
        try:
            category_pk = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            result = use_case.execute(
                request=GetCategoryRequest(id=category_pk)
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category = {
            "id": str(result.id),
            "name": result.name,
            "description": result.description,
            "is_active": result.is_active
        }

        return Response(status=HTTP_200_OK, data=category)
