from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    STANDARD = settings.USER_ROLE_STANDARD
    OWNER = settings.USER_ROLE_OWNER
    MANAGER = settings.USER_ROLE_MANAGER
    MEDIA_MANAGER = settings.USER_ROLE_MEDIA_MANAGER

    ROLE_CHOICES = (
        (1, 'Owner'),
        (2, 'Standard'),
        (3, 'Manager'),
        (4, 'Media Manager')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


    def __str__(self):
        return self.email + f"(role-{self.role})"