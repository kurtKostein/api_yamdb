from django.shortcuts import render
from rest_framework import filters, mixins, viewsets

from .models import Categories, Genres, Titles
from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
