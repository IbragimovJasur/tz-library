import rest_framework_simplejwt.token_blacklist.admin as blacklist_admin

from django.contrib import admin

from apps.users.models import (
    BaseUser,
    Client,
    Author,
)


# JWT token settings
class CustomOutstandingTokenAdmin(blacklist_admin.OutstandingTokenAdmin):
    # allowing admin deleting database OutstandingTokens
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(blacklist_admin.OutstandingToken)
admin.site.register(blacklist_admin.OutstandingToken, CustomOutstandingTokenAdmin)


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_active", "is_staff", "is_superuser")


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(Client)
admin.site.register(Author)
