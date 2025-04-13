from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreateForm
from django.contrib.auth.models import Group
from .models import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserCreateForm
    add_form = UserCreateForm

    list_display = ('phone_number', 'id_card', )
    list_filter = ('is_seller', 'is_active')

    fieldsets = (
        ('Main', {'fields': ('phone_number', 'password', 'first_name', 'last_name', 'age')}),
        ("Permissions", {"fields": ["is_staff", "is_active", "is_seller",]}),
    )

    add_fieldsets = (
        ('Main', {'fields': ('phone_number', 'password1', 'password2', 'id_card', 'first_name', 'last_name', 'age')}),
    )

    search_fields = ('phone_number', 'id_card',)
    ordering = ('phone_number', 'id_card')
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
