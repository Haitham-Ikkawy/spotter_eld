from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


from helper.common.constants import TripStatus, LocationType
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    current_cycle_used = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(70)]  # 70-hour limit
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def calculate_total_on_duty_hours(self, days=8):
        """
        Calculate the total on-duty hours for the last `days` days.
        Includes driving time, pickup/drop-off time, and fueling time.
        """
        now = timezone.now()
        start_date = now - timedelta(days=days)

        # Get all trips within the last `days` days
        trips = Trip.objects.filter(driver=self, start_dt__gte=start_date)

        total_on_duty_hours = 0
        for trip in trips:
            total_on_duty_hours += trip.total_on_duty_hours()

        return total_on_duty_hours

    def is_compliant_with_70_hour_rule(self):
        """
        Check if the driver is compliant with the 70-hour/8-day rule.
        """
        return self.calculate_total_on_duty_hours(days=8) < 70

    def is_compliant_with_14_hour_window(self, trip_start_time):
        """
        Check if the driver is within the 14-hour driving window.
        """
        # Get the last trip end time (or last off-duty time)
        last_trip = Trip.objects.filter(driver=self).order_by('-end_dt').first()
        if not last_trip or not last_trip.end_dt:
            return True  # No previous trips, compliant by default

        # Calculate the 14-hour window
        window_end_time = last_trip.end_dt + timedelta(hours=14)
        return trip_start_time <= window_end_time


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)  # Vehicle Identification Number
    current_mileage = models.IntegerField(default=0)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.name} {self.model}"


class Location(models.Model):
    TYPE_CHOICES = (
        (LocationType.TRIP_START, "Trip Start"),
        (LocationType.TRIP_END, "Trip End"),
        (LocationType.FUELING, "Fueling"),
        (LocationType.BREAK_REST, "Break Rest"),
    )
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=LocationType.TRIP_START)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    STATUS_CHOICES = (
        (TripStatus.ONGOING, "Ongoing"),
        (TripStatus.ENDED, "Ended"),
    )
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    start_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='start_trips')
    end_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='end_trips')
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(blank=True, null=True)
    pickup_start_dt = models.DateTimeField(blank=True, null=True)
    pickup_end_dt = models.DateTimeField(blank=True, null=True)
    pickup_duration = models.FloatField(default=60, help_text="Pickup duration in minutes", null=True, blank=True)
    drop_off_start_dt = models.DateTimeField(blank=True, null=True)
    drop_off_end_dt = models.DateTimeField(blank=True, null=True)
    drop_off_duration = models.FloatField(default=60, help_text="Drop-off duration in minutes", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=TripStatus.ONGOING)
    violations = models.TextField(blank=True, null=True)
    distance = models.FloatField(help_text="Distance in miles")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.id} by {self.driver.name}"

    def total_driving_hours(self):
        """
        Calculate total driving hours for this trip.
        """
        if self.end_dt and self.start_dt:
            return (self.end_dt - self.start_dt).total_seconds() / 3600  # Convert to hours
        return 0

    def total_on_duty_hours(self):
        """
        Calculate total on-duty hours for this trip (driving + pickup + drop-off).
        """
        driving_hours = self.total_driving_hours()
        pickup_hours = self.pickup_duration / 60  # Convert minutes to hours
        drop_off_hours = self.drop_off_duration / 60  # Convert minutes to hours
        return driving_hours + pickup_hours + drop_off_hours


class DriverHos(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    total_driving_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(11)]  # 11-hour driving limit
    )
    total_on_duty_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(14)]  # 14-hour on-duty limit
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Log for {self.driver.name} on {self.date}"


class RestBreak(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='restbreaks')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='restbreaks')
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(help_text="Duration in minutes", null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rest break for {self.trip.driver.name} on {self.trip.start_dt.date()}"


class Fueling(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='fuelings')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='fuelings')
    amount = models.FloatField(help_text="Fuel amount in gallons")
    cost = models.FloatField(help_text="Fuel cost in dollars")
    duration = models.FloatField(help_text="Duration in minutes", null=True, blank=True)
    mileage_at_fueling = models.IntegerField(help_text="Mileage at the time of fueling")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fueling for Trip {self.trip.id} at {self.location.name}"