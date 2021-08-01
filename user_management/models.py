from django.db import models
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
