# from rest_framework import viewsets
#
# from spotter_eld.models import Driver, Vehicle, Location, Trip, DriverLog, RestBreak, Fueling
# from .serializers import (
#     DriverSerializer, VehicleSerializer, LocationSerializer,
#     TripSerializer, DriverLogSerializer, RestBreakSerializer, FuelingSerializer
# )
#
#
# # Driver ViewSet
# class DriverViewSet(viewsets.ModelViewSet):
#     queryset = Driver.objects.all()
#     serializer_class = DriverSerializer
#
#
# # Vehicle ViewSet
# class VehicleViewSet(viewsets.ModelViewSet):
#     queryset = Vehicle.objects.all()
#     serializer_class = VehicleSerializer
#
#
# # Location ViewSet
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
#
#
# # Trip ViewSet
# class TripViewSet(viewsets.ModelViewSet):
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#
#
# # DriverLog ViewSet
# class DriverLogViewSet(viewsets.ModelViewSet):
#     queryset = DriverLog.objects.all()
#     serializer_class = DriverLogSerializer
#
#
# # RestBreak ViewSet
# class RestBreakViewSet(viewsets.ModelViewSet):
#     queryset = RestBreak.objects.all()
#     serializer_class = RestBreakSerializer
#
#
# # Fueling ViewSet
# class FuelingViewSet(viewsets.ModelViewSet):
#     queryset = Fueling.objects.all()
#     serializer_class = FuelingSerializer


from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helper.common.constants import RequestTypes
from spotter_eld.models import Driver, Vehicle, Location, Trip, RestBreak, Fueling
from .serializers import (
    DriverSerializer, VehicleSerializer, LocationSerializer,
    TripSerializer, DriverLogSerializer, RestBreakSerializer, TripListSerializer
)


# Driver API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def driver_list(request):
    if request.method in RequestTypes.GET:
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vehicle API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    if request.method in RequestTypes.GET:
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Location API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def location_list(request):
    if request.method in RequestTypes.GET:
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
def location_detail(request, pk):
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


# Trip API


# DriverLog API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def driverlog_list(request):
    if request.method in RequestTypes.GET:
        logs = DriverLog.objects.all()
        serializer = DriverLogSerializer(logs, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        serializer = DriverLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
def driverlog_detail(request, pk):
    log = get_object_or_404(DriverLog, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = DriverLogSerializer(log)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = DriverLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# RestBreak API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def restbreak_list(request):
    if request.method in RequestTypes.GET:
        restbreaks = RestBreak.objects.all()
        serializer = RestBreakSerializer(restbreaks, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        serializer = RestBreakSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
def restbreak_detail(request, pk):
    restbreak = get_object_or_404(RestBreak, pk=pk)

    if request.method in RequestTypes.GET:
        serializer = RestBreakSerializer(restbreak)
        return Response(serializer.data)

    if request.method in RequestTypes.PUT:
        serializer = RestBreakSerializer(restbreak, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method in RequestTypes.DELETE:
        restbreak.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Fueling API
@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])
def fueling_list(request):
    if request.method in RequestTypes.GET:
        fuelings = Fueling.objects.all()


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
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


@api_view([RequestTypes.GET, RequestTypes.POST])
@permission_classes([IsAuthenticated])  # Require authentication
def trip_list(request):
    if request.method in RequestTypes.GET:
        trips = Trip.objects.select_related('driver', 'vehicle').all()
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data)

    if request.method in RequestTypes.POST:
        data = request.data.copy()  # Make a mutable copy of request data
        data['start_dt'] = now()  # Override start_time with server timestamp

        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.GET, RequestTypes.PUT, RequestTypes.DELETE])
@permission_classes([IsAuthenticated])
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
