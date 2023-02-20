from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from tag.models import Tag
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIV2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RecipeAPIV2Detail(APIView):
    def get_object(self):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=self.kwargs.get('pk')
        )
        return recipe

    def get(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_object(),
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_object(),
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
