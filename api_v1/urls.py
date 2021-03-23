from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


router = DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(r'titles/(?P<titles_id>\d+)', TitlesViewSet)
router.register('categories/{slug}', CategoriesViewSet)
router.register('genres/{slug}', GenresViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
