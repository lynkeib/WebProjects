from rest_framework import serializers
from profile_api import models
from profile_api.models import UserProfile


class HelloSerializer(serializers.Serializer):
    """Serializers a name filed for testing APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"}
            }
        }

    def create(self, validated_data: dict) -> UserProfile:
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance: UserProfile, validated_data: dict) -> UserProfile:
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.Serializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "create_on")
        extra_kwargs = {"user_profile": {"read_only": True}}
