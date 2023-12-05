"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry

from core import models


class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    ]

    readonly_fields = (
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )
    search_fields = [
        'object_id',
        'object_repr',
        'change_message'
    ]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['first_name', 'last_name', 'email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
            )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'), {'fields': ('last_login',)},
        ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
            }),
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "company_url",
        "address_1",
        "phone_number",
        "mobile_number",
    ]

    search_fields = [
        "company_name",
        "company_url",
        "address_1"
    ]


class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "client",
        "status",
    ]

    raw_id_fields = ['user']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'client__company_name',
    ]

    list_filter = (
        ('client', admin.RelatedFieldListFilter),
    )

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    first_name.short_description = "First name"
    last_name.short_description = "Last name"
    email.short_description = "Email"


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Account, AccountAdmin)
