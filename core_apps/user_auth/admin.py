from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserChangeForm, UserCreationForm
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role"
    ]
    list_filter = ["is_staff", "is_active", "role","email"]
    fieldsets = (
        (
            _("Login Crendetials"),
            {
                "fields":(
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Info"),
            {
                "fields":(
                    "first_name","last_name","middle_name","role","id_no"
                )
            },
        ),
        (
        _("Account Status"),
        {
            "fields": (
                "account_status",
                "failed_login_attempts"
            )
        },
        ),
        (
        _("Security"),
        {
            "fields":(
                "security_question","security_answer"  ) },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields":(
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                    "is_active",
                )
            }
        ),
        (
            _("Important dates"),
            {
                "fields":(
                    "last_login",
                    "date_joined"

                )
            },
        ),
    )
search_fields = ['email',"username","first_name","last_name"]
ordering=["email"]