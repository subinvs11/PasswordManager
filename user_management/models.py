from django.db import models
from django.conf import settings
from fernet_fields import EncryptedTextField
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(BaseModel, AbstractUser):
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.first_name


class Organization(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_owner', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="organization_members", blank=True)

    class Meta:
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class PersonalPassword(BaseModel):
    site = models.CharField(max_length=200)
    login_url = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    password = EncryptedTextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='personal_password_owner', on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="personal_password_users", blank=True)

    class Meta:
        verbose_name_plural = "Personal Passwords"
        unique_together = ('site', 'owner')

    def __str__(self):
        return self.site


class OrganizationPasswordAccessLevel(models.Model):

    ACCESS_CHOICES = (
        (1, 'View'),
        (2, 'Edit'),
    )

    organization_password = models.ForeignKey('OrganizationPassword',
                                              related_name='organization_password_access_levels',
                                              on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_password_user',
                             on_delete=models.SET_NULL, null=True, blank=True)
    access_level = models.IntegerField(choices=ACCESS_CHOICES, default=1)


class OrganizationPassword(BaseModel):
    site = models.CharField(max_length=200)
    login_url = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    password = EncryptedTextField()
    organization = models.ForeignKey(Organization, related_name='organization_password_organization',
                                     on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='OrganizationPasswordAccessLevel',
                                   related_name="organization_password_users", blank=True)

    class Meta:
        verbose_name_plural = "Organization Passwords"
        unique_together = ('site', 'organization')

    def __str__(self):
        return self.site
