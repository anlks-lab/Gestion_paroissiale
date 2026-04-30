from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import  User,  UserActivity


class UserAdmin(BaseUserAdmin):
    # model = User
    list_display = (
        "username",
        "email",
        "sacrement",
        "role",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser", "role")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "sacrement",
                    "profile_picture",
                    "phone_number",
                    "adresse",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "created_at","updated_at"), },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "sacrement",
                    "password1",
                    "password2",
                    'role',
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name', "sacrement")
    ordering = ("username",)
    readonly_fields = ["updated_at","created_at"]

class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'user__username', 'details')
    readonly_fields = ('user', 'action', 'details', 'ip_address', 'user_agent', 'timestamp')


admin.site.register(User, UserAdmin)
admin.site.register(UserActivity,UserActivityAdmin)
