from django.db import models
from django.contrib.auth.models import AbstractUser


class RidegroupUser(AbstractUser):
    firebase_uid = models.CharField(max_length=128, null=False, blank=False)
    setup_complete = models.BooleanField(default=False, null=False)
    username = models.CharField(max_length=32, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    photo_url = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=False)

    def public_profile(self):
        return {'firstName': self.first_name, 'username': self.username}

    def complete_profile(self):
        return {'firstName': self.first_name, 'lastName': self.last_name, 'username': self.username,
                'setupComplete': self.setup_complete, 'email': self.email, 'phone': self.phone,
                'photoUrl': self.photo_url}
