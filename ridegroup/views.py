import json
import re
from typing import Union

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import Q, QuerySet
from django.http import HttpResponse, JsonResponse, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ridegroup.serializers import *


@api_view(['GET'])
def connection_test(request: HttpRequest) -> HttpResponse:
    print(request.headers)
    print(request.user)
    return HttpResponse('pong')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login(request: HttpRequest) -> JsonResponse:
    user = RidegroupUser.objects.get(id=request.user.id)
    serializer = MyUserSerializer(user)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request: HttpRequest) -> JsonResponse:
    user = RidegroupUser.objects.get(id=request.user.id)
    if user.setup_complete or not (
            'email' in request.POST and 'username' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST):
        return JsonResponse('', status=status.HTTP_400_BAD_REQUEST)
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
def create_ride(request: HttpRequest) -> HttpResponse:
    user = RidegroupUser.objects.get(id=request.user.id)
    if not user.setup_complete:
        return HttpResponse('User not set up', status=status.HTTP_400_BAD_REQUEST)
    ride = json.loads(request.body)
    ride['id'] = Ride.objects.order_by('id').last()
    ride['id'] = 0 if ride['id'] is None else ride['id'].id + 1
    ride['owner'] = user.id
    ride['vehicle'] = ride['vehicle']['id']
    serializer = MyRideSerializer(data=ride)
    if not serializer.is_valid():
        print(serializer.errors)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    new = serializer.save()
    return HttpResponse(new.id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_vehicles(request: HttpRequest) -> JsonResponse:
    user = RidegroupUser.objects.get(id=request.user.id)
    vehicles = Vehicle.objects.filter(user=user).all()
    if len(vehicles) == 0:
        return JsonResponse('', safe=False)
    serializer = VehicleSerializer(vehicles, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle(request: HttpRequest) -> HttpResponse:
    formatted = json.loads(request.body)
    formatted['user'] = request.user.id
    formatted['id'] = Vehicle.objects.order_by('id').last()
    formatted['id'] = 0 if formatted['id'] is None else formatted['id'].id + 1
    serializer = VehicleSerializer(data=formatted)
    if not serializer.is_valid():
        print(serializer.errors)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    new = serializer.save()
    return HttpResponse(new.id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_rides(request: HttpRequest) -> JsonResponse:
    rides = Ride.objects.filter(owner=RidegroupUser.objects.get(id=request.user.id)).all()
    return JsonResponse(serialize_public_rides(rides), safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_search(request: HttpRequest) -> JsonResponse:
    try:
        post = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse('', status=status.HTTP_400_BAD_REQUEST, safe=False)
    query = Q()
    if 'latitude' not in post or 'longitude' not in post:
        return JsonResponse('', status=status.HTTP_400_BAD_REQUEST, safe=False)
    initial_point = Point(post['longitude'], post['latitude'])
    if 'title' in post:
        query |= Q(title__contains=post['title'])
    if 'start_loc_name' in post:
        query |= Q(start_loc__contains=post['start_loc_name'])
    if 'end_loc_name' in post:
        query |= Q(end_loc__contains=post['end_loc_name'])
    if 'max_start_dist' in post:
        max_dist = float(re.sub(r'\D', '', post['max_start_dist']))
        if post['max_start_dist'][-1] == 'm':
            query &= Q(start_loc__distance_lt=(initial_point, Distance(m=max_dist)))
        elif post['max_start_dist'][-2:] == 'km':
            query &= Q(start_loc__distance_lt=(initial_point, Distance(km=max_dist)))
        elif post['max_start_dist'][-2:] == 'yd':
            query &= Q(start_loc__distance_lt=(initial_point, Distance(yd=max_dist)))
        elif post['max_start_dist'][-2:] == 'mi':
            query &= Q(start_loc__distance_lt=(initial_point, Distance(mi=max_dist)))
        else:
            print('invalid units in distance {}'.format(post['max_start_dist']))
    if 'max_end_dist' in post:
        max_dist = float(re.sub(r'\D', '', post['max_end_dist']))
        if post['max_end_dist'][-1] == 'm':
            query &= Q(end_loc__distance_lt=(initial_point, Distance(m=max_dist)))
        elif post['max_end_dist'][-2:] == 'km':
            query &= Q(end_loc__distance_lt=(initial_point, Distance(km=max_dist)))
        elif post['max_end_dist'][-2:] == 'yd':
            query &= Q(end_loc__distance_lt=(initial_point, Distance(yd=max_dist)))
        elif post['max_end_dist'][-2:] == 'mi':
            query &= Q(end_loc__distance_lt=(initial_point, Distance(mi=max_dist)))
        else:
            print('invalid units in distance {}'.format(post['max_end_dist']))
    rides = Ride.objects.filter(query).all()
    return JsonResponse(serialize_public_rides(rides), safe=False)


def serialize_public_rides(rides: Union[Ride, QuerySet]) -> str:
    if rides is None:
        return ''
    serializer = RideSerializer(rides, many=True)
    return serializer.data
