from django.contrib import admin

# Register your models here.
from user_management.models import CustomUser, Organization, PersonalPassword, OrganizationPassword, \
    OrganizationPasswordAccessLevel


admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(PersonalPassword)
admin.site.register(OrganizationPassword)
admin.site.register(OrganizationPasswordAccessLevel)