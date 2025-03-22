from datetime import timedelta

from django.db.models import F, Sum, ExpressionWrapper, fields, Q
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helper.common.constants import RequestTypes, TripStatus, LocationType
from helper.decorators.api_decorators import driver_profile_required
from spotter_eld.models import Vehicle, Location, Trip, Driver
from .serializers import (
    VehicleSerializer, LocationSerializer,
    TripSerializer, TripListSerializer
)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])  # Require authentication
@driver_profile_required
def get_trips(request):
    # Ensure the authenticated user has a driver profile

    driver = request.user.driver_profile
    trip_id = request.GET.get("trip_id")

    q_set = Q(driver=driver)

    if trip_id:
        q_set &= Q(pk=trip_id)

    trips = Trip.objects.filter(q_set).select_related('driver', 'vehicle')
    serializer = TripListSerializer(trips, many=True)
    return Response(serializer.data)


@api_view([RequestTypes.GET])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_trip_form_data(request):
    """
    Fetches all necessary data for the trip form submission:
    - Drivers
    - Vehicles
    - Locations
    """
    try:
        # drivers = Driver.objects.all()
        locations = Location.objects.filter(type__in=[LocationType.TRIP_START, LocationType.TRIP_END])
        unallocated_vehicles = Vehicle.objects.exclude(trips__status=TripStatus.ONGOING)

        # driver_serializer = DriverSerializer(drivers, many=True)
        vehicle_serializer = VehicleSerializer(unallocated_vehicles, many=True)
        location_serializer = LocationSerializer(locations, many=True)

        # Validate the 70-hour/8-day limit
        last_8_days = now() - timedelta(days=8)
        driver = request.user.driver_profile
        # Calculate total hours worked
        total_hours_worked = (
                Trip.objects.filter(driver=driver, end_dt__isnull=False, start_dt__gte=last_8_days)
                .annotate(work_duration=ExpressionWrapper(F('end_dt') - F('start_dt'), output_field=fields.DurationField()))
                .aggregate(total_hours=Sum(ExpressionWrapper(F('work_duration') / timedelta(hours=1), output_field=fields.FloatField())))
                ['total_hours'] or 0
        )

        if total_hours_worked >= 70:
            return Response(
                {"error": "Driver has reached the 70-hour limit for the last 8 days. Cannot start a new trip."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            # "drivers": driver_serializer.data,
            "vehicles": vehicle_serializer.data,
            "locations": location_serializer.data,
            "current_cycle_used": total_hours_worked
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view([RequestTypes.POST])
@permission_classes([IsAuthenticated])  # Require authentication
@driver_profile_required
def create_trip(request):
    # Ensure the authenticated user has a driver profile

    driver = request.user.driver_profile
    vehicle_id = request.data.get("vehicle")
    start_location = request.data.get("start_location")
    end_location = request.data.get("end_location")

    # Validate start_location and end_location are different
    if start_location == end_location:
        return Response(
            {"error": "Start location and end location must be different."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check if the driver already has an ongoing trip
    if Trip.objects.filter(driver=driver, status=TripStatus.ONGOING).exists():
        return Response(
            {"error": "Driver already has an ongoing trip. Cannot create another one."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the vehicle is already assigned to an ongoing trip
    if Trip.objects.filter(vehicle_id=vehicle_id, status=TripStatus.ONGOING).exists():
        return Response(
            {"error": "Vehicle is already assigned to an ongoing trip. Cannot assign it to another."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate the 70-hour/8-day limit
    last_8_days = now() - timedelta(days=8)

    # Calculate total hours worked
    total_hours_worked = (
            Trip.objects.filter(driver=driver, end_dt__isnull=False, start_dt__gte=last_8_days)
            .annotate(work_duration=ExpressionWrapper(F('end_dt') - F('start_dt'), output_field=fields.DurationField()))
            .aggregate(total_hours=Sum(ExpressionWrapper(F('work_duration') / timedelta(hours=1), output_field=fields.FloatField())))
            ['total_hours'] or 0
    )

    if total_hours_worked >= 70:
        return Response(
            {"error": "Driver has reached the 70-hour limit for the last 8 days. Cannot start a new trip."},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data.copy()
    data['start_dt'] = now()  # Set start time as the current timestamp
    data['driver'] = driver.id  # Use the driver's ID directly

    serializer = TripSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view([RequestTypes.PUT])
@permission_classes([IsAuthenticated])
@driver_profile_required
def update_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    serializer = TripSerializer(trip, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_pickup(request):
    try:

        data = request.data.copy()

        trip = Trip.objects.get(id=data.get('id'))
        # Ensure the trip is ongoing and pickup is not yet completed
        if trip.pickup_start_dt:
            return Response(
                {"error": "Pickup already ended for this trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if trip.status != TripStatus.ONGOING:
            return Response(
                {"error": "Cannot end pickup for a non-ongoing trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate pickup duration
        trip.pickup_start_dt = now()
        trip.save()

        return Response(
            {"message": "Pickup ended successfully.", "pickup_duration": trip.pickup_duration},
            status=status.HTTP_200_OK
        )

    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_pickup(request):
    try:

        data = request.data.copy()

        trip = Trip.objects.get(id=data.get('id'))
        # Ensure the trip is ongoing and pickup is not yet completed
        if trip.pickup_end_dt:
            return Response(
                {"error": "Pickup already ended for this trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if trip.status != TripStatus.ONGOING:
            return Response(
                {"error": "Cannot end pickup for a non-ongoing trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate pickup duration
        trip.pickup_end_dt = now()
        pickup_duration = (trip.pickup_end_dt - trip.pickup_start_dt).total_seconds() / 3600  # Convert to hours
        trip.pickup_duration = max(1.0, round(pickup_duration, 2))  # Minimum 1 hour
        trip.save()

        return Response(
            {"message": "Pickup ended successfully.", "pickup_duration": trip.pickup_duration},
            status=status.HTTP_200_OK
        )

    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def start_drop_off(request):
    try:
        data = request.data.copy()

        trip = Trip.objects.get(id=data.get('id'))

        # Ensure the trip is ongoing and pickup is not yet completed
        if trip.drop_off_start_dt:
            return Response(
                {"error": "Drop Off already started for this trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if trip.status != TripStatus.ONGOING:
            return Response(
                {"error": "Cannot end pickup for a non-ongoing trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate pickup duration
        trip.drop_off_start_dt = now()
        trip.save()

        return Response(
            {"message": "Drop Off started successfully."},
            status=status.HTTP_200_OK
        )

    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def end_drop_off(request):
    try:
        data = request.data.copy()

        trip = Trip.objects.get(id=data.get('id'))

        # Ensure the trip is ongoing and pickup is not yet completed
        if trip.drop_off_end_dt:
            return Response(
                {"error": "Drop Off already ended for this trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if trip.status != TripStatus.ONGOING:
            return Response(
                {"error": "Cannot end Drop Off for a non-ongoing trip."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate pickup duration
        trip.drop_off_end_dt = now()
        trip.end_dt = now()
        trip.status = TripStatus.ENDED
        drop_off_duration = (trip.drop_off_end_dt - trip.drop_off_start_dt).total_seconds() / 3600  # Convert to hours
        trip.drop_off_duration = max(1.0, round(drop_off_duration, 2))  # Minimum 1 hour
        trip.save()

        return Response(
            {"message": "Drop Off ended successfully.", "Drop Off": trip.drop_off_duration},
            status=status.HTTP_200_OK
        )

    except Trip.DoesNotExist:
        return Response(
            {"error": "Trip not found."},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def can_create_trip(request):
    driver = request.user.driver_profile

    # Check if the driver already has an ongoing trip
    if Trip.objects.filter(driver=driver, status=TripStatus.ONGOING).exists():
        return Response(
            {"error": "Driver already has an ongoing trip. Cannot create another one."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate the 70-hour/8-day limit
    last_8_days = now() - timedelta(days=8)

    # Calculate total hours worked
    total_hours_worked = (
            Trip.objects.filter(driver=driver, end_dt__isnull=False, start_dt__gte=last_8_days)
            .annotate(work_duration=ExpressionWrapper(F('end_dt') - F('start_dt'), output_field=fields.DurationField()))
            .aggregate(total_hours=Sum(ExpressionWrapper(F('work_duration') / timedelta(hours=1), output_field=fields.FloatField())))
            ['total_hours'] or 0
    )

    if total_hours_worked >= 70:
        return Response(
            {"error": "Driver has reached the 70-hour limit for the last 8 days. Cannot start a new trip."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:

        return Response({"can_create_trip": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_trip_trace(request):
    # Fetch the trip

    trip_id = request.GET.get("id")
    trip = get_object_or_404(Trip.objects.prefetch_related('restbreaks', 'fuelings'), id=trip_id)

    actions = []

    # Trip Start
    actions.append({
        "type": "Trip Start",
        "_dt": trip.start_dt,
        "location": serialize_location(trip.start_location),
        "duration": None
    })

    # Rest Breaks
    for rest in trip.restbreaks.all():
        actions.append({
            "type": "Rest Break",
            "_dt": rest.start_dt,
            "location": serialize_location(rest.location),
            "duration": rest.duration
        })

    # Fueling
    for fuel in trip.fuelings.all():
        actions.append({
            "type": "Fueling",
            "_dt": fuel.created_dt,
            "location": serialize_location(fuel.location),
            "duration": fuel.duration
        })

    # Trip End
    if trip.end_dt:
        actions.append({
            "type": "Trip End",
            "_dt": trip.end_dt,
            "location": serialize_location(trip.end_location),
            "duration": None
        })

    # Sort all actions by datetime (_dt)
    actions = sorted(actions, key=lambda x: x["_dt"])

    return Response({
        "trip_id": trip.id,
        "driver": trip.driver.id,
        "actions": actions
    })
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_driver_log_sheet(request):
    driver = request.user.driver_profile
    log_date = request.GET.get("date")

    if not log_date:
        return Response({"error": "date is required."}, status=400)

    # Fetch driver and logs
    driver = get_object_or_404(Driver.objects.prefetch_related('trips', 'hos_logs'), id=driver.id)
    last_8_days = now() - timedelta(days=8)
    trips = driver.trips.filter(start_dt__gte=last_8_days)
    hos_logs = driver.hos_logs.filter(date=log_date)

    # Initialize log data
    log_data = {
        "driver": {
            "name": driver.name,
            "license": driver.license_number,
        },
        "date": log_date,
        "logs": [],
        "trip_events": [],
        "daily_recap": {
            "total_driving_hours": 0,
            "total_on_duty_hours": 0,
            "hours_available_tomorrow": 14,  # Default value
            "miles_driven": 0,
        }
    }

    # Process HOS logs
    for log in hos_logs:
        log_data["daily_recap"]["total_driving_hours"] += log.total_driving_hours
        log_data["daily_recap"]["total_on_duty_hours"] += log.total_on_duty_hours

        # Add driving and on-duty logs
        log_data["logs"].append({
            "startHour": log.start_dt.hour,
            "endHour": log.end_dt.hour if log.end_dt else log.start_dt.hour + int(log.total_driving_hours),
            "status": "Driving"
        })
        log_data["logs"].append({
            "startHour": log.start_dt.hour,
            "endHour": log.end_dt.hour if log.end_dt else log.start_dt.hour + int(log.total_on_duty_hours),
            "status": "On Duty"
        })

    # Process trips
    for trip in trips:
        # Trip Start
        log_data["trip_events"].append({
            "type": "Trip Start",
            "timestamp": trip.start_dt.isoformat(),
            "location": serialize_location(trip.start_location),
            "odometer": trip.vehicle.current_mileage,
        })

        # Rest Breaks
        for rest in trip.restbreaks.all():
            log_data["trip_events"].append({
                "type": "Rest Break",
                "timestamp": rest.start_dt.isoformat(),
                "location": serialize_location(rest.location),
                "odometer": trip.vehicle.current_mileage,
            })

        # Fueling Events
        for fuel in trip.fuelings.all():
            log_data["trip_events"].append({
                "type": "Fueling",
                "timestamp": fuel.created_dt.isoformat(),
                "location": serialize_location(fuel.location),
                "odometer": fuel.mileage_at_fueling,
            })

        # Trip End
        if trip.end_dt:
            log_data["trip_events"].append({
                "type": "Trip End",
                "timestamp": trip.end_dt.isoformat(),
                "location": serialize_location(trip.end_location),
                "odometer": trip.vehicle.current_mileage,
            })

    # Calculate miles driven (sum of trip distances)
    log_data["daily_recap"]["miles_driven"] = sum(trip.distance for trip in trips)

    return Response(log_data)

def serialize_location(location):
    if location:
        return {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "name": location.name,
        }
    return None


urls = [
    path('get_trips', get_trips, name='get_trips'),
    path('get_trip_form_data', get_trip_form_data, name='get_trip_form_data'),
    path('create_trip', create_trip, name='create_trip'),
    path('update_trip', update_trip, name='update_trip'),
    path('start_pickup', start_pickup, name='start_pickup'),
    path('end_pickup', end_pickup, name='end_pickup'),
    path('can_create_trip', can_create_trip, name='end_pickup'),
    path('start_drop_off', start_drop_off, name='start_drop_off'),
    path('end_drop_off', end_drop_off, name='end_drop_off'),
    path('get_trip_trace', get_trip_trace, name='get_trip_trace'),
    path('get_driver_log_sheet', get_driver_log_sheet, name='get_driver_log_sheet'),
]
