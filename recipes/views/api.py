from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from tag.models import Tag
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from ..permissions import IsOwner


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 5


class RecipeAPIV2ViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        qs = Recipe.objects.get_published()
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def list(self, request, *args, **kwargs):
        if self.get_queryset().exists() is False:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ('DELETE', 'PATCH'):
            return [IsOwner(), ]
        return super().get_permissions()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = RecipeSerializer(
            instance=obj,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
