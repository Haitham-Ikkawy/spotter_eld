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
from datetime import timedelta

from django.db.models import Q
from django.urls import path
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helper.common.constants import RequestTypes, LocationType, TripStatus
from helper.decorators.api_decorators import driver_profile_required
from spotter_eld.models import RestBreak, Location, Trip
from .serializers import (
    RestBreakSerializer, TripListSerializer, LocationSerializer, RestBreakListSerializer
)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_rest_break(request):
    driver = request.user.driver_profile
    fueling_id = request.GET.get("fueling_id")

    q_set = Q(trip__driver=driver)

    if fueling_id:
        q_set &= Q(pk=fueling_id)

    fueling = RestBreak.objects.filter(q_set).select_related('trip', 'location')

    serializer = RestBreakListSerializer(fueling, many=True)

    return Response(serializer.data)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_rest_break_form_data(request):
    """
    Fetches all necessary data for the trip form submission:
    - Drivers
    - Vehicles
    - Locations
    """

    driver = request.user.driver_profile
    try:
        # drivers = Driver.objects.all()
        locations = Location.objects.filter(type=LocationType.BREAK_REST)
        trip_obj = Trip.objects.filter(driver=driver, status=TripStatus.ONGOING)

        # driver_serializer = DriverSerializer(drivers, many=True)
        trip_serializer = TripListSerializer(trip_obj, many=True)
        location_serializer = LocationSerializer(locations, many=True)

        return Response({
            "trips": trip_serializer.data,
            "locations": location_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view([RequestTypes.POST])
@permission_classes([IsAuthenticated])  # Require authentication
@driver_profile_required
def create_rest_break(request):
    data = request.data.copy()
    driver = request.user.driver_profile

    data['start_dt'] = now()  # Set start time as the current timestamp
    data['driver'] = driver.id  # Use the driver's ID directly

    serializer = RestBreakSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_rest_break(request):
    try:
        _now = now()

        data = request.data.copy()

        rest_break = RestBreak.objects.get(id=data.get('id'))
        # Ensure the trip is ongoing and pickup is not yet completed
        if rest_break.end_dt:
            return Response(
                {"error": "Rest Break already ended for this trip."},
                status=status.HTTP_400_BAD_REQUEST
            )


        # Calculate rest_break duration
        rest_break.end_dt = _now
        rest_break.duration = (_now - rest_break.end_dt).total_seconds() / 60  # Convert to hours
        rest_break.save()

        return Response(
            {"message": "Rest Break ended successfully.", "rest_break": rest_break.duration},
            status=status.HTTP_200_OK
        )

    except Trip.DoesNotExist:
        return Response(
            {"error": "Rest Break not found."},
            status=status.HTTP_404_NOT_FOUND
        )

urls = [
    path('get_rest_break', get_rest_break, name='get_rest_break'),
    path('get_rest_break_form_data', get_rest_break_form_data, name='get_rest_break_form_data'),
    path('create_rest_break', create_rest_break, name='create_rest_break'),
    path('end_rest_break', end_rest_break, name='end_rest_break'),
]
