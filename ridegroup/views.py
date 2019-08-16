from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ridegroup.authentication import FirebaseAuthentication
from ridegroup.models import *
from ridegroup.serializers import *
import json


@api_view(['GET'])
def connection_test(request):
    print(request.headers)
    print(request.user)
    return HttpResponse('pong')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login(request):
    user = RidegroupUser.objects.get(id=request.user.id)
    serializer = MyUserSerializer(user)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):
    user = RidegroupUser.objects.get(id=request.user.id)
    if user.setup_complete or not (
            'email' in request.POST and 'username' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST):
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.username = request.POST['username'].replace(r'\w', '')
    if 'phone' in request.POST:
        user.phone = request.POST['phone']
    user.setup_complete = True
    user.save()
    serializer = MyUserSerializer(user)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ride(request):
    user = RidegroupUser.objects.get(id=request.user.id)
    if not user.setup_complete:
        return HttpResponse('User not set up', status=status.HTTP_400_BAD_REQUEST)
    ride = json.loads(request.body)
    ride['id'] = Ride.objects.order_by('id').last()
    ride['id'] = 0 if ride['id'] is None else ride['id'].id + 1
    ride['owner'] = ride['owner']['id']
    ride['vehicle'] = ride['vehicle']['id']
    serializer = RideSerializer(data=ride)
    if not serializer.is_valid():
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    new = serializer.save()
    return HttpResponse(new.id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_vehicles(request):
    user = RidegroupUser.objects.get(id=request.user.id)
    vehicles = Vehicle.objects.filter(user=user).all()
    if len(vehicles) == 0:
        return JsonResponse('', safe=False)
    serializer = VehicleSerializer(vehicles, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle(request):
    formatted = json.loads(request.body)
    formatted['user'] = request.user.id
    formatted['id'] = Vehicle.objects.order_by('id').last()
    formatted['id'] = 0 if formatted['id'] is None else formatted['id'].id + 1
    serializer = VehicleSerializer(data=formatted)
    if not serializer.is_valid():
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    new = serializer.save()
    return HttpResponse(new.id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_rides(request):
    rides = list(Ride.objects.filter(owner=RidegroupUser.objects.get(id=request.user.id)).all())
    if rides is None or len(rides) == 0:
        return JsonResponse('', safe=False)
    serializer = MyRidesSerializer(rides, many=len(rides) > 1)
    return JsonResponse(serializer.data, safe=False)
