from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles/(?P<titles_id>\d+)', TitleViewSet)
router.register('categories/{slug}', CategoryViewSet)
router.register('genres/{slug}', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
