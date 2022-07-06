from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomBaseUserManager
from apps.users.utils import (
    get_client_photo_upload_path,
    get_author_photo_upload_path,
)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """Base model for all user models"""

    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        verbose_name=_("Email address"),
        unique=True,
        error_messages={"unique": "User with entered email already exists"},
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=100,
        unique=True,
        error_messages={"unique": "User with entered username already exists"},
        validators=[username_validator],
    )
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = CustomBaseUserManager()
    REQUIRED_FIELDS = ["username", "full_name"]

    class Meta:
        db_table = "base_users"

    def __str__(self):
        return self.username


class Client(models.Model):
    """Client is regular user who can borrow and read books from library"""

    user = models.OneToOneField(
        verbose_name=_("Base User"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        related_query_name="client"
    )
    photo = models.ImageField(
        verbose_name=_("Profile Photo"),
        upload_to=get_client_photo_upload_path,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        verbose_name=_("Birthday"), 
        null=True, 
        blank=True
    )

    class Meta:
        db_table = "clients"

    def __str__(self):
        return self.user.username


class Author(models.Model):
    user = models.OneToOneField(
        verbose_name=_("Base User"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authors",
        related_query_name="author"   
    )
    photo = models.ImageField(
        verbose_name=_("Profile Photo"),
        upload_to=get_author_photo_upload_path
    )
    country = models.CharField(
        verbose_name=_("Where are you from?"),
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name=_("About the author"),
        null=True,
        blank=True
    )

    class Meta:
        db_table = "authors"

    def __str__(self):
        return self.user.username
