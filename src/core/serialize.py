from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.validators import UniqueValidator

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError('Password mismatch')
        return attrs

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = PasswordField(required=True)

    def validate(self, attrs):
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'password is wrong'})
        return attrs

    def create(self, validated_data) -> User:
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance



