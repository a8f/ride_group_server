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
        fields = ['id', 'username', 'first_name', 'date_joined', 'photo_url', 'last_name']


class MyUserSerializer(serializers.ModelSerializer):
    """
    Serializer for RidegroupUser containing all private user information
    Should only be shown to the user being serialized
    """

    class Meta:
        model = RidegroupUser
        fields = ['id', 'setup_complete', 'username', 'first_name', 'date_joined', 'photo_url', 'last_name', 'email',
                  'phone', 'last_login']


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for Vehicle
    """

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)

    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'make', 'model', 'year', 'seats', 'doors', 'color', 'plate', 'user']


class RideSerializer(serializers.ModelSerializer):
    passengers = BaseUserSerializer(many=True, read_only=True)
    owner = BaseUserSerializer(many=False, read_only=True)
    vehicle = VehicleSerializer(many=False, read_only=True)

    def create(self, validated_data):
        return Ride.objects.create(**validated_data)

    class Meta:
        model = Ride
        fields = ['owner', 'start_loc', 'start_long', 'start_lat', 'end_loc', 'end_long', 'end_lat', 'time', 'vehicle',
                  'passengers', 'id']


class MyRidesSerializer(serializers.ModelSerializer):
    passengers = BaseUserSerializer(many=True, read_only=True)
    owner = BaseUserSerializer(many=False, read_only=True)
    vehicle = VehicleSerializer(many=False, read_only=True)

    def create(self, validated_data):
        return Ride.objects.create(**validated_data)

    class Meta:
        model = Ride
        fields = ['owner', 'start_loc', 'start_long', 'start_lat', 'end_loc', 'end_long', 'end_lat', 'time', 'vehicle',
                  'passengers', 'id', 'title', 'description']
