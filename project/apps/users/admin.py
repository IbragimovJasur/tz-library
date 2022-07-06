from django.contrib import admin

from apps.users.models import (
    BaseUser,
    Client,
    Author,
)


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_active", "is_staff", "is_superuser")


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(Client)
admin.site.register(Author)
