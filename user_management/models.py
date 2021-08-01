from django.db import models
from django.conf import settings
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
