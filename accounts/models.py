from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name="customuser_groups", blank=True
    )
    age = models.PositiveIntegerField(null=True, blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_permissions", blank=True
    )