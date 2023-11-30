from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)
    confirmation_code = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'password',
            'confirmation_code',
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        existing_user = User.objects.filter(
            username=attrs.get('username')
        ).first()
        if existing_user:
            if (
                attrs.get('confirmation_code')
                != existing_user.confirmation_code
            ):
                raise serializers.ValidationError("Wrong confirmation code.")

        return super(MyTokenObtainSerializer, self).validate(attrs)
