from rest_framework import serializers

from apps.users.models import Client
from apps.users.utils.db_utils import (
    create_base_user_instance,
    create_client_user_instance,
    update_base_user_instance,
    update_client_or_author_user_instance,
)
from apps.users.utils.validation_utils import (
    is_taken_email,
    is_taken_username,
    is_taken_email_and_not_same_with_instance_email,
    is_taken_username_and_not_same_with_instance_username,
)
from apps.users.utils.base_utils import remove_base_user_related_inputs


class ClientUserCreateSerializer(serializers.ModelSerializer):
    """For handling POST requests for Client user profile create endpoint"""

    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username", max_length=100)
    full_name = serializers.CharField(
        source="user.full_name", 
        max_length=150, 
        allow_blank=True
    )
    password = serializers.CharField(
        source="user.password", max_length=128, write_only=True
    )

    class Meta:
        model = Client
        fields = ("email", "username", "full_name", "birthday", "photo", "password")

    def create(self, validated_data):
        base_user_instance = create_base_user_instance(
            validated_data.get("user")
        )
        validated_data_without_base_user_fields = remove_base_user_related_inputs(
            validated_data
        )
        client_user_instance = create_client_user_instance(
            base_user_instance, validated_data_without_base_user_fields
        )
        return client_user_instance

    def validate_email(self, value):
        return is_taken_email(value)
    
    def validate_username(self, value):
        return is_taken_username(value)


class ClientUserUpdateSerializer(serializers.ModelSerializer):
    """For handling PUT and PATCH requests for Client user profile endpoint"""

    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username", max_length=100)
    full_name = serializers.CharField(
        source="user.full_name", 
        max_length=150, 
        allow_blank=True
    )

    class Meta:
        model = Client
        fields = ("email", "username", "full_name", "birthday", "photo")

    def update(self, instance, validated_data):
        base_user_instance = self.context["request"].user
        base_user_update_fields = validated_data.get("user", {})  # default is {}

        # updating base user model instance
        update_base_user_instance(base_user_instance, base_user_update_fields)
        # updating client user instance
        updated_client_user_instance = update_client_or_author_user_instance(
            instance, validated_data
        )
        return updated_client_user_instance
    
    def validate_email(self, value):
        base_user = self.context["request"].user
        return is_taken_email_and_not_same_with_instance_email(
            value, base_user
        )
    
    def validate_username(self, value):
        base_user = self.context["request"].user
        return is_taken_username_and_not_same_with_instance_username(
            value, base_user
        )
    