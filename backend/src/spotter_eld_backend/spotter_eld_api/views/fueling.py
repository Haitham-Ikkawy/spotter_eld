from django.db.models import Q, Max
from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helper.common.constants import RequestTypes, TripStatus, LocationType
from helper.decorators.api_decorators import driver_profile_required
from spotter_eld.models import Location, Fueling, Trip
from .serializers import (
    LocationSerializer,
    FuelingSerializer, FuelingListSerializer, TripListSerializer
)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_fueling(request):
    driver = request.user.driver_profile
    fueling_id = request.GET.get("fueling_id")

    q_set = Q(trip__driver=driver)

    if fueling_id:
        q_set &= Q(pk=fueling_id)

    fueling = Fueling.objects.filter(q_set).select_related('trip', 'location')

    serializer = FuelingListSerializer(fueling, many=True)

    return Response(serializer.data)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_fueling_form_data(request):
    """
    Fetches all necessary data for the trip form submission:
    - Drivers
    - Vehicles
    - Locations
    """

    driver = request.user.driver_profile
    try:
        # drivers = Driver.objects.all()
        locations = Location.objects.filter(type=LocationType.FUELING)
        trip_obj = Trip.objects.filter(driver=driver, status=TripStatus.ONGOING)

        # driver_serializer = DriverSerializer(drivers, many=True)
        trip_serializer = TripListSerializer(trip_obj, many=True)
        location_serializer = LocationSerializer(locations, many=True)

        return Response({
            # "drivers": driver_serializer.data,_form_
            "trips": trip_serializer.data,
            "locations": location_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view([RequestTypes.POST])
@permission_classes([IsAuthenticated])  # Require authentication
@driver_profile_required
def create_fueling(request):
    driver = request.user.driver_profile
    data = request.data.copy()

    trip_id = data.get('trip')
    current_mileage = int(data.get('mileage_at_fueling'))
    trip = Trip.objects.get(id=trip_id, driver=driver)

    # Get the maximum mileage from previous fuelings for the same trip
    last_fueling_mileage = (
        Fueling.objects.filter(trip=trip)
        .aggregate(max_mileage=Max('mileage_at_fueling'))
        .get('max_mileage')
    )

    # If there's a previous fueling, check the mileage difference
    if last_fueling_mileage is not None and current_mileage - last_fueling_mileage > 1000:
        return Response(
            {"error": "Fueling must occur at least once every 1,000 miles."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = FuelingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



urls = [
    path('get_fueling', get_fueling, name='get_fueling'),
    path('get_fueling_form_data', get_fueling_form_data, name='get_fueling_form_data'),
    path('create_fueling', create_fueling, name='create_fueling')
]
