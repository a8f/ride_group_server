from rest_framework import serializers

from ridegroup.models import RidegroupUser


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
