from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from helper.common.constants import RequestTypes
from spotter_eld.models import Driver, Vehicle, Location, Trip
from .serializers import (
    DriverSerializer, VehicleSerializer, LocationSerializer,
    TripSerializer
)


@api_view([RequestTypes.GET, RequestTypes.POST])
def trip_list(request):
    if request.method in RequestTypes.GET:
        trips = Trip.objects.select_related('driver', 'vehicle').all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        data = request.data.copy()  # Make a mutable copy of request data
        data['start_time'] = now()  # Override start_time with server timestamp
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view([RequestTypes.GET])
def trip_form_data(request):
    """
    Fetches all necessary data for the trip form submission:
    - Drivers
    - Vehicles
    - Locations
    """
    try:
        drivers = Driver.objects.all()
        vehicles = Vehicle.objects.all()
        locations = Location.objects.all()

        driver_serializer = DriverSerializer(drivers, many=True)
        vehicle_serializer = VehicleSerializer(vehicles, many=True)
        location_serializer = LocationSerializer(locations, many=True)

        return Response({
            "drivers": driver_serializer.data,
            "vehicles": vehicle_serializer.data,
            "locations": location_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
