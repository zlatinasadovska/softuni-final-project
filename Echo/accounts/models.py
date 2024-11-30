from django.contrib.auth.models import AbstractUser
from django.db import models
from Echo.accounts.managers import UserProfileManager


class UserProfile(AbstractUser):
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    is_artist = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
