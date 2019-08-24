from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from ridegroup.models import *


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for RidegroupUser with only id, username, and first name
    """

    class Meta:
        model = RidegroupUser
        fields = ['id', 'username', 'first_name']


class RelatedUserSerializer(serializers.ModelSerializer):
    """
    Serializer for RidegroupUser containing some identifying user information
    """

    class Meta:
        model = RidegroupUser
        fields = ['id', 'username', 'first_name', 'date_joined', 'photo_url', 'last_name', 'rides_driver',
                  'rides_passenger', 'rating_driver', 'rating_passenger']


class MyUserSerializer(serializers.ModelSerializer):
    """
    Serializer for RidegroupUser containing all private user information
    Should only be shown to the user being serialized
    """

    class Meta:
        model = RidegroupUser
        fields = ['id', 'setup_complete', 'username', 'first_name', 'date_joined', 'photo_url', 'last_name', 'email',
                  'phone', 'last_login', 'rides_driver', 'rides_passenger', 'rating_driver', 'rating_passenger']


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for Vehicle
    """

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)

    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'make', 'model', 'year', 'seats', 'doors', 'color', 'plate', 'user']


class MyRideSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated user's own rides
    """
    passengers = BaseUserSerializer(many=True, read_only=True)
    start_loc = PointField(required=True)
    end_loc = PointField(required=True)

    def create(self, validated_data):
        return Ride.objects.create(**validated_data)

    class Meta:
        model = Ride
        fields = ['owner', 'start_loc_name', 'end_loc_name', 'start_loc', 'end_loc', 'time', 'vehicle',
                  'passengers', 'id', 'title', 'description']


class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for public rides
    """
    passengers = BaseUserSerializer(many=True, read_only=True)
    owner = BaseUserSerializer(many=False, read_only=True)
    vehicle = VehicleSerializer(many=False, read_only=True)
    start_loc = PointField(required=True)
    end_loc = PointField(required=True)

    class Meta:
        model = Ride
        fields = ['owner', 'start_loc_name', 'end_loc_name', 'start_loc', 'end_loc', 'time', 'vehicle',
                  'passengers', 'id', 'title', 'description']
