from django.db import models
from django.contrib.auth.models import AbstractUser


class RidegroupUser(AbstractUser):
    firebase_uid = models.CharField(max_length=128, null=False, blank=False)
    setup_complete = models.BooleanField(default=False, null=False)
    email = models.CharField(max_length=64, null=False, blank=False, unique=True)
    username = models.CharField(max_length=32, null=True, blank=True, unique=False)
    phone = models.CharField(max_length=16, null=True, blank=True)
    photo_url = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'firebase_uid']
