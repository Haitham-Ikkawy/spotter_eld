from django.shortcuts import get_object_or_404
from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helper.common.constants import RequestTypes
from helper.decorators.api_decorators import driver_profile_required
from spotter_eld.models import Location
from .serializers import (
    LocationSerializer
)


@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
@driver_profile_required
def create_location(request):

    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_or_update_location(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        location.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


urls = [
    path('get_locations', get_locations, name='get_locations'),
    path('create_location', create_location, name='create_location'),
    path('get_or_update_location', get_or_update_location, name='get_or_update_location'),
]
