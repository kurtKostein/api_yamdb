from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class ConfirmationCodeField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'confirmation_code'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class EmailCodeTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _(
            'No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = ConfirmationCodeField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        confirmation_code = attrs.get('confirmation_code', '')

        users = User.objects.filter(
            email=email,
            confirmation_code=confirmation_code
        )
        if users.exists():
            self.user = users.first()
            return {}

        raise exceptions.AuthenticationFailed(
            self.error_messages['no_active_account'],
            'no_active_account',
        )

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement "get_token" method '
            'for "TokenObtainSerializer" subclasses')


class EmailCodeTokenObtainPairSerializer(EmailCodeTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'slug']


class CategoryRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer()
        return serializer.to_representation(value)


class GenreRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer()
        return serializer.to_representation(value)


class TitleSerializer(serializers.ModelSerializer):

    category = CategoryRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    genre = GenreRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    title_id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
