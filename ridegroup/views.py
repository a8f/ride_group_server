from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ridegroup.authentication import FirebaseAuthentication
from .models import *


@api_view(['GET'])
def connection_test(request):
    print(request.headers)
    print(request.user)
    return HttpResponse('pong')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login(request):
    return JsonResponse(RidegroupUser.objects.get(id=request.user.id).complete_profile())
