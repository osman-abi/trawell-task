"""Account Serializing file for create APIs"""
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import User

# pylint: disable=R0903


class UserSerializer(serializers.ModelSerializer):
    """All info about User"""

    class Meta:
        """Initializing fields and model"""

        model = User
        fields = [
            "id",
            "email",
            "username",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """This class will be used for registration"""

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        "username": "The username should only contain alphanumeric characters"
    }

    class Meta:
        """Initializing fields and model"""

        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """This class will be used for login User"""

    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    is_superuser = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        """Initializing fields and model"""

        model = User
        fields = ["id", "email", "password", "username", "tokens", "is_superuser"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
            "id": user.id,
        }
