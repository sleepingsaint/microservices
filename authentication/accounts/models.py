from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import UserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=10, unique=True, null=True)
    
    first_name = models.CharField(max_length=10, null=True, blank=True)
    last_name = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
