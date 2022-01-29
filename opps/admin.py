from django.contrib import admin
from .models import User, InterestedIn, Organization, Role


class InterestedInInline(admin.TabularInline):
    model = InterestedIn
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [InterestedInInline]


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [RoleInline]
