from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    EmailCodeTokenObtainPairView, GenreViewSet, ReviewViewSet,
                    send_confirmation_code, TitleViewSet, UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles/(?P<titles_id>\d+)', TitleViewSet)
router.register('categories/{slug}', CategoryViewSet)
router.register('genres/{slug}', GenreViewSet)
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_refresh'
    ),
    path(
        'auth/email/',
        send_confirmation_code,
        name='send_confirmation_code'
    )
]
