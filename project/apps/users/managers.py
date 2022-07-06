from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomBaseUserManager(BaseUserManager):
    """Custom manager for BaseUser model"""

    use_in_migrations = True

    def _create_user(
        self, email, username, full_name, password, **extra_fields
    ):
        if not email:
            raise ValueError("Email is not set")
        if not username:
            raise ValueError("Username is not set")
        if not full_name:
            raise ValueError("Full Name is not set")

        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email, username, full_name, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, username, full_name, password, **extra_fields
        )

    def create_superuser(
        self, email, username, full_name, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            email, username, full_name, password, **extra_fields
        )
