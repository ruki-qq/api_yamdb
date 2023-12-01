from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    @staticmethod
    def validate_username(value):
        """Checks that username is not in forbidden values."""

        forbidden = ['me']

        if value in forbidden:
            raise serializers.ValidationError(f'Username cannot be "{value}"')
        return value


class UserSerializer(RegistrationSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        existing_user = User.objects.filter(
            username=attrs.get('username')
        ).first()
        if existing_user:
            conf_code = attrs.get('confirmation_code')
            if not existing_user.confirmation_code or not check_password(
                conf_code, existing_user.confirmation_code
            ):
                raise serializers.ValidationError("Wrong confirmation code.")

        return super(MyTokenObtainSerializer, self).validate(attrs)
