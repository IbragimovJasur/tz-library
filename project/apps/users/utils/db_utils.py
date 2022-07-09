from django.contrib.auth.hashers import make_password  # for hashing password

from apps.users.models import BaseUser
from apps.users.models import Client
from apps.users.models import Author


def create_base_user_instance(base_user_instance_create_data) -> BaseUser:
    """Function for creating BaseUser model instance"""
    password = base_user_instance_create_data.pop("password")
    
    base_user_instance = BaseUser.objects.create(
        password=make_password(password),  # hashing
        **base_user_instance_create_data
    )
    return base_user_instance


def create_client_or_author_user_instance(
    model: Client | Author, 
    base_user_instance: BaseUser, 
    validated_data_without_base_user_fields
) -> Client | Author:
    """Function for creating Client or Author user model instance"""

    client_user_instance = model.objects.create(
        user=base_user_instance, 
        **validated_data_without_base_user_fields
    )
    return client_user_instance


def update_base_user_instance(
    base_user: BaseUser, base_user_update_fields: dict
) -> None:
    """Function for updating BaseUser model instance"""

    for field_name, field_value in base_user_update_fields.items():
        setattr(base_user, field_name, field_value)
    base_user.save()   


def update_client_or_author_user_instance(
    client_or_author_user_instance: Client | Author, validated_data: dict
) -> Client | Author:
    """For updating Client or Author user instance"""

    for field_name, field_value in validated_data.items():
        setattr(client_or_author_user_instance, field_name, field_value)
    client_or_author_user_instance.save()
    
    return client_or_author_user_instance
