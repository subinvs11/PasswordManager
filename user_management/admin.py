from django.contrib import admin

# Register your models here.
from user_management.models import CustomUser, Organization


admin.site.register(CustomUser)
admin.site.register(Organization)