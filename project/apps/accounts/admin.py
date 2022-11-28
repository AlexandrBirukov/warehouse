from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext as _

from project.apps.accounts.models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(UserAdmin):
    change_form_template = 'loginas/change_form.html'
    form = CustomUserChangeForm
    list_display = ('email', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'phone',
            'uid_key',
            'metadata',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('uid_key',)
