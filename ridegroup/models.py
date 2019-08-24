from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.utils import timezone


class RidegroupUser(AbstractUser):
    firebase_uid = models.CharField(max_length=128, null=False, blank=False)
    setup_complete = models.BooleanField(default=False, null=False)
    email = models.CharField(max_length=64, null=False, blank=False, unique=True)
    username = models.CharField(max_length=32, null=True, blank=True, unique=False)
    phone = models.CharField(max_length=16, null=True, blank=True)
    photo_url = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=False)
    rides_driver = models.PositiveIntegerField(default=0, null=False)
    rides_passenger = models.PositiveIntegerField(default=0, null=False)
    rating_driver = models.FloatField(default=-1, null=False)
    rating_passenger = models.FloatField(default=-1, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'firebase_uid']


class Ride(models.Model):
    owner = models.ForeignKey('RidegroupUser', on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(default=timezone.now, null=False, blank=True)
    start_loc_name = models.CharField(max_length=128, null=False)
    start_loc = models.PointField(null=False)
    end_loc_name = models.CharField(max_length=128, null=False)
    end_loc = models.PointField(null=False)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(null=False)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=999)

    def passengers(self):
        return Passenger.objects.filter(ride=self).all()


class Passenger(models.Model):
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE, null=False, blank=False, related_name='passengers')
    user = models.ForeignKey('RidegroupUser', on_delete=models.CASCADE)
    seat = models.SmallIntegerField(null=False)


class Vehicle(models.Model):
    name = models.CharField(max_length=32, null=False)
    make = models.CharField(max_length=32, null=False)
    model = models.CharField(max_length=32, null=False)
    seats = models.PositiveSmallIntegerField(default=4, null=False)
    doors = models.PositiveSmallIntegerField(default=4, null=False)
    color = models.CharField(max_length=32, null=False)
    plate = models.CharField(max_length=16, null=False, unique=True)
    verified = models.BooleanField(default=False, null=False)
    year = models.SmallIntegerField(default=None, null=True)
    user = models.ForeignKey('RidegroupUser', on_delete=models.CASCADE, null=False)
