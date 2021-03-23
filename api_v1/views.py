from django.shortcuts import render
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from .models import Categories, Genres, Titles
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer)
from .permissions import IsAdminOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']
    permission_classes = (IsAdminOrReadOnly, )


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = (IsAdminOrReadOnly, )


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = (IsAdminOrReadOnly, )
