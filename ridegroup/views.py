from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ridegroup.authentication import FirebaseAuthentication
from ridegroup.models import *
from ridegroup.serializers import *


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
