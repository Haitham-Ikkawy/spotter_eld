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
from spotter_eld.models import Vehicle, Location, Trip, Driver, DriverHos, RestBreak, Fueling
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
@driver_profile_required
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
@driver_profile_required
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

        # Calculate pickup duration in minutes
        trip.pickup_end_dt = now()
        pickup_duration_minutes = (trip.pickup_end_dt - trip.pickup_start_dt).total_seconds() / 60  # Convert to minutes
        trip.pickup_duration = max(60, round(pickup_duration_minutes, 2))  # Minimum 60 minutes

        # Check for violations
        violations = []
        if trip.pickup_duration > 60:
            violations.append(f"Pickup duration exceeded: {trip.pickup_duration} minutes")

        # Save violations
        trip.violations = ", ".join(violations) if violations else ""  # Store as a comma-separated string
        trip.save()

        return Response(
            {
                "message": "Pickup ended successfully.",
                "pickup_duration": trip.pickup_duration,
                "violations": trip.violations
            },
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

        driver = request.user.driver_profile

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
        drop_off_duration = (trip.drop_off_end_dt - trip.drop_off_start_dt).total_seconds() / 60  # Convert to minutes
        trip.drop_off_duration = max(60, round(drop_off_duration, 2))  # Minimum 1 hour
        # Check for violations
        violations = [trip.violations]
        if trip.drop_off_duration > 60:
            violations.append(f"Drop off duration exceeded: {trip.drop_off_duration} minutes")

        # Save violations
        trip.violations = ", ".join(violations) if violations else ""  # Store as a comma-separated string
        trip.save()

        # Calculate total driving and on-duty hours for the trip
        total_driving_hours = trip.total_driving_hours()
        total_on_duty_hours = trip.total_on_duty_hours()

        # Create a DriverHos record for the trip
        driver_hos = DriverHos.objects.create(
            driver=driver,
            date=trip.start_dt.date(),
            total_driving_hours=total_driving_hours,
            total_on_duty_hours=total_on_duty_hours
        )

        if trip and driver_hos:
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

    driver_obj = Driver.objects.filter(pk=driver.id).first()

    # Calculate total hours worked
    total_hours_worked = (
            Trip.objects.filter(driver=driver, end_dt__isnull=False, start_dt__gte=last_8_days)
            .annotate(work_duration=ExpressionWrapper(F('end_dt') - F('start_dt'), output_field=fields.DurationField()))
            .aggregate(total_hours=Sum(ExpressionWrapper(F('work_duration') / timedelta(hours=1), output_field=fields.FloatField())))
            ['total_hours'] or 0
    )

    driver_obj.current_cycle_used = total_hours_worked
    driver_obj.save()
    driver_obj.refresh_from_db()

    if driver_obj.current_cycle_used >= 70:
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@driver_profile_required
def get_driver_log_sheet(request):
    driver = request.user.driver_profile
    log_date = request.GET.get("date")

    if not log_date:
        return Response({"error": "date is required."}, status=400)

    try:
        # Fetch driver and related data
        trips = Trip.objects.filter(driver=driver, created_dt__date=log_date)
        rest_breaks = RestBreak.objects.filter(trip__driver=driver, created_dt__date=log_date)
        fuelings = Fueling.objects.filter(trip__driver=driver, created_dt__date=log_date)

        # Initialize log data structure
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
            },
            "total_hours": {
                "Off Duty": 0,
                "Sleeper Berth": 0,
                "Driving": 0,
                "On Duty": 0,
            },
            "remarks": [],
        }

        # Process trips
        for trip in trips:
            # Add trip start event
            log_data["trip_events"].append({
                "type": "Trip Start",
                "timestamp": trip.start_dt.isoformat(),
                "location": trip.start_location.name,
                "odometer": trip.vehicle.current_mileage,
            })

            # Add trip end event
            if trip.end_dt:
                log_data["trip_events"].append({
                    "type": "Trip End",
                    "timestamp": trip.end_dt.isoformat(),
                    "location": trip.end_location.name,
                    "odometer": trip.vehicle.current_mileage,
                })

            # Add driving hours to daily recap
            driving_hours = trip.total_driving_hours()
            log_data["daily_recap"]["total_driving_hours"] += driving_hours
            log_data["total_hours"]["Driving"] += driving_hours

            # Add on-duty hours to daily recap
            on_duty_hours = trip.total_on_duty_hours()
            log_data["daily_recap"]["total_on_duty_hours"] += on_duty_hours
            log_data["total_hours"]["On Duty"] += on_duty_hours

            # Add miles driven
            log_data["daily_recap"]["miles_driven"] += trip.distance

            # Add remarks for trip locations
            log_data["remarks"].append(trip.start_location.name)
            log_data["remarks"].append(trip.end_location.name)

        # Process rest breaks
        for rest in rest_breaks:
            # Add rest break event
            log_data["trip_events"].append({
                "type": "Rest Break",
                "timestamp": rest.start_dt.isoformat(),
                "location": rest.location.name,
                "odometer": rest.trip.vehicle.current_mileage,
            })

            # Add rest break hours to total hours
            rest_hours = rest.duration / 60 if rest.duration else 0  # Convert minutes to hours
            log_data["total_hours"]["Sleeper Berth"] += rest_hours

        # Process fuelings
        for fuel in fuelings:
            # Add fueling event
            log_data["trip_events"].append({
                "type": "Fuel Stop",
                "timestamp": fuel.created_dt.isoformat(),
                "location": fuel.location.name,
                "odometer": fuel.mileage_at_fueling,
            })

        # Generate logs based on duty status changes
        log_data["logs"] = generate_duty_status_logs(driver, log_date)

        # Format daily recap hours
        log_data["daily_recap"]["total_driving_hours"] = f"{log_data['daily_recap']['total_driving_hours']} hrs"
        log_data["daily_recap"]["total_on_duty_hours"] = f"{log_data['daily_recap']['total_on_duty_hours']} hrs"
        log_data["daily_recap"]["miles_driven"] = f"{log_data['daily_recap']['miles_driven']} miles"

        return Response(log_data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def generate_duty_status_logs(driver, log_date):
#     """
#     Generate logs based on duty status changes for the driver on the specified date.
#     """
#     logs = []
#
#     # Fetch all duty status changes for the driver on the specified date
#     trips = Trip.objects.filter(driver=driver, start_dt__date=log_date).order_by('start_dt')
#     rest_breaks = RestBreak.objects.filter(trip__driver=driver, start_dt__date=log_date).order_by('start_dt')
#
#     # Initialize variables to track duty status changes
#     current_status = "Off Duty"
#     current_start_time = None
#
#     # Process trips and rest breaks to generate logs
#     for trip in trips:
#         # Add Off Duty to Driving transition
#         if current_status == "Off Duty":
#             logs.append({
#                 "startHour": current_start_time.hour if current_start_time else 0,
#                 "endHour": trip.start_dt.hour,
#                 "status": current_status,
#             })
#             current_status = "Driving"
#             current_start_time = trip.start_dt
#
#         # Add Driving to On Duty transition (e.g., after pickup/drop-off)
#         if trip.pickup_start_dt and trip.pickup_end_dt:
#             logs.append({
#                 "startHour": trip.start_dt.hour,
#                 "endHour": trip.pickup_start_dt.hour,
#                 "status": "Driving",
#             })
#             logs.append({
#                 "startHour": trip.pickup_start_dt.hour,
#                 "endHour": trip.pickup_end_dt.hour,
#                 "status": "On Duty",
#             })
#             current_status = "Driving"
#             current_start_time = trip.pickup_end_dt
#
#         # Add Driving to Off Duty transition (e.g., after trip ends)
#         if trip.end_dt:
#             logs.append({
#                 "startHour": current_start_time.hour,
#                 "endHour": trip.end_dt.hour,
#                 "status": current_status,
#             })
#             current_status = "Off Duty"
#             current_start_time = trip.end_dt
#
#     # Process rest breaks to add Sleeper Berth status
#     for rest in rest_breaks:
#         logs.append({
#             "startHour": rest.start_dt.hour,
#             "endHour": rest.end_dt.hour if rest.end_dt else rest.start_dt.hour + 3,  # Default 3 hours
#             "status": "Sleeper Berth",
#         })
#
#     # Add the final Off Duty status if needed
#     if current_status != "Off Duty":
#         logs.append({
#             "startHour": current_start_time.hour,
#             "endHour": 24,  # End of the day
#             "status": current_status,
#         })
#
#     return logs


def generate_duty_status_logs(driver, log_date):
    """
    Generate logs based on duty status changes for the driver on the specified date.
    """
    logs = []

    # Fetch all duty status changes for the driver on the specified date
    trips = Trip.objects.filter(driver=driver, start_dt__date=log_date).order_by('start_dt')
    rest_breaks = RestBreak.objects.filter(trip__driver=driver, start_dt__date=log_date).order_by('start_dt')

    # Initialize variables to track duty status changes
    current_status = "Off Duty"
    current_start_time = None

    # Process trips and rest breaks to generate logs
    for trip in trips:
        # Convert start and end times to quarter-hour precision
        start_hour = trip.start_dt.hour + (trip.start_dt.minute / 60.0)
        pickup_start_hour = trip.pickup_start_dt.hour + (trip.pickup_start_dt.minute / 60.0) if trip.pickup_start_dt else None
        pickup_end_hour = trip.pickup_end_dt.hour + (trip.pickup_end_dt.minute / 60.0) if trip.pickup_end_dt else None
        end_hour = trip.end_dt.hour + (trip.end_dt.minute / 60.0) if trip.end_dt else None

        # Add Off Duty to Driving transition
        if current_status == "Off Duty":
            logs.append({
                "startHour": current_start_time.hour + (current_start_time.minute / 60.0) if current_start_time else 0,
                "endHour": start_hour,
                "status": current_status,
            })
            current_status = "Driving"
            current_start_time = trip.start_dt

        # Add Driving to On Duty transition (e.g., after pickup/drop-off)
        if trip.pickup_start_dt and trip.pickup_end_dt:
            logs.append({
                "startHour": start_hour,
                "endHour": pickup_start_hour,
                "status": "Driving",
            })
            logs.append({
                "startHour": pickup_start_hour,
                "endHour": pickup_end_hour,
                "status": "On Duty",
            })
            current_status = "Driving"
            current_start_time = trip.pickup_end_dt

        # Add Driving to Off Duty transition (e.g., after trip ends)
        if trip.end_dt:
            logs.append({
                "startHour": current_start_time.hour + (current_start_time.minute / 60.0),
                "endHour": end_hour,
                "status": current_status,
            })
            current_status = "Off Duty"
            current_start_time = trip.end_dt

    # Process rest breaks to add Sleeper Berth status
    for rest in rest_breaks:
        rest_start_hour = rest.start_dt.hour + (rest.start_dt.minute / 60.0)
        rest_end_hour = rest.end_dt.hour + (rest.end_dt.minute / 60.0) if rest.end_dt else rest_start_hour + 0.25  # Default 15 minutes

        logs.append({
            "startHour": rest_start_hour,
            "endHour": rest_end_hour,
            "status": "Sleeper Berth",
        })

    # Add the final Off Duty status if needed
    if current_status != "Off Duty":
        logs.append({
            "startHour": current_start_time.hour + (current_start_time.minute / 60.0),
            "endHour": 24.0,  # End of the day
            "status": current_status,
        })

    return logs


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
