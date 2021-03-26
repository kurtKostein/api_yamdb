from rest_framework.pagination import PageNumberPagination
from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailCodeTokenObtainPairSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserSerializer)
from .permissions import IsAdmin, IsAdminOrReadOnly
from .models import Category, Comment, Genre, Review, Title, User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import filters, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4


class EmailCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailCodeTokenObtainPairSerializer
    permission_classes = []


@api_view(['POST'])
@permission_classes([])
def send_confirmation_code(request):
    email = request.data.get('email', '')
    if not email:
        return Response(
            data={'error': 'Не передан email'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=uuid4(),
            email=email,
            confirmation_code=uuid4()
        )
    success = send_mail(
        'Yamdb registration',
        f'Your confirmation code: {user.confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        (email,)
    )
    if success:
        return Response(
            data={'message': 'Код выслан на email'},
            status=status.HTTP_200_OK
        )
    return Response(
        data={'error': 'Не удалось отправить код на email'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            serializer = self.get_serializer(request.user)

        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
