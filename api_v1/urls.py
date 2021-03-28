from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet,
                    EmailCodeTokenObtainPairView, GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet, send_confirmation_code)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'^titles/(?P<titles_id>\d+)', TitleViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(
    r'^reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/token/',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh',
        EmailCodeTokenObtainPairView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/auth/email/',
        send_confirmation_code,
        name='send_confirmation_code'
    )
]
