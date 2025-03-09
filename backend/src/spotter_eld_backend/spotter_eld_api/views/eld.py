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
from rest_framework.decorators import api_view
from rest_framework.response import Response

from spotter_eld.models import Driver, Vehicle, Location, Trip, DriverLog, RestBreak, Fueling
from .serializers import (
    DriverSerializer, VehicleSerializer, LocationSerializer,
    TripSerializer, DriverLogSerializer, RestBreakSerializer
)


# Driver API
@api_view(['GET', 'POST'])
def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vehicle API
@api_view(['GET', 'POST'])
def vehicle_list(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Location API
@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Trip API


@api_view(['GET'])
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


@api_view(['GET', 'POST'])
def trip_list(request):
    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()  # Make a mutable copy of request data
        data['start_time'] = now()  # Override start_time with server timestamp
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# DriverLog API
@api_view(['GET', 'POST'])
def driverlog_list(request):
    if request.method == 'GET':
        logs = DriverLog.objects.all()
        serializer = DriverLogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DriverLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def driverlog_detail(request, pk):
    log = get_object_or_404(DriverLog, pk=pk)

    if request.method == 'GET':
        serializer = DriverLogSerializer(log)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DriverLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# RestBreak API
@api_view(['GET', 'POST'])
def restbreak_list(request):
    if request.method == 'GET':
        restbreaks = RestBreak.objects.all()
        serializer = RestBreakSerializer(restbreaks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RestBreakSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def restbreak_detail(request, pk):
    restbreak = get_object_or_404(RestBreak, pk=pk)

    if request.method == 'GET':
        serializer = RestBreakSerializer(restbreak)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RestBreakSerializer(restbreak, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        restbreak.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Fueling API
@api_view(['GET', 'POST'])
def fueling_list(request):
    if request.method == 'GET':
        fuelings = Fueling.objects.all()
