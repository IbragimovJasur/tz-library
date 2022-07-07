from rest_framework.serializers import ValidationError

from apps.users.models import BaseUser


def is_taken_email(email: str):
    """Checking BaseUser model instance exists with entered email."""

    if BaseUser.objects.filter(email=email).exists():
        raise ValidationError(
            detail={"email": "User with entered email already exists"}
        )
    return email


def is_taken_username(username: str) -> bool:
    """Checking Client model instance exists with entered username."""

    if BaseUser.objects.filter(username=username).exists():
        raise ValidationError(
            detail={"username": "User with entered username already exists"}
        )
    return username


def is_taken_email_and_not_same_with_instance_email(
    email: str, instance: BaseUser
):
    """
    Raise error if there is another client user that has same email field 
    value, with the email field value that client is inputed to update.
    """

    if (BaseUser.objects.filter(email=email).exists() and 
            not (email == instance.email)):
        raise ValidationError(
            {"email": "User with entered email already exists"}
        )
    return email


def is_taken_username_and_not_same_with_instance_username(
    username: str, instance: BaseUser
):
    """
    Raise error if there is another client user that has same username field 
    value, with the username field value that client is inputed to update.
    """

    if (BaseUser.objects.filter(username=username).exists()
            and not username == instance.username):
        raise ValidationError(
            {"username": "User with entered username already exists"}
        )
    return username
