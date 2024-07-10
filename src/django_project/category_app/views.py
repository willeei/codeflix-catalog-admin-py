from uuid import uuid4

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(status=HTTP_200_OK, data=[
            {
                'id': uuid4(),
                'name': 'Category 1',
                'description': 'Category 1 description',
                'is_active': True
            },
            {
                'id': uuid4(),
                'name': 'Category 2',
                'description': 'Category 2 description',
                'is_active': True
            }
        ])
