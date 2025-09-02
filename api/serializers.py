from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DogImage

# ----------- User Serializers -----------

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  # now required

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": True},
        }

    def create(self, validated_data):
        # Use Django's built-in create_user (handles hashing properly)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],  # email is required now
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# ----------- Dog Image Serializer -----------

class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogImage
        fields = ["id", "user", "image", "predicted_breed", "uploaded_at"]
        read_only_fields = ["id", "user", "predicted_breed", "uploaded_at"]