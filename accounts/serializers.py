# apps/accounts/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import  User, UserActivity


class UserSerializer(serializers.ModelSerializer):
   

    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "sacrement",
            "username",
            "profile_picture",
            "profile_picture_url",
            "is_active",
            "is_verified",
            "created_at",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "last_login",
            "profile_picture_url",
        ]

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return self.context["request"].build_absolute_uri(obj.profile_picture.url)
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"new_password": "Les mots de passe ne correspondent pas."}
            )
        return data


class UserActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user_email",
            "user_full_name",
            "action",
            "action_display",
            "details",
            "ip_address",
            "timestamp",
        ]
        read_only_fields = fields
