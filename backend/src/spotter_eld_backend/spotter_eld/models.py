from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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
        (LocationType.BREAK_REST, "break Rest"),
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
    start_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='start_trips'
    )
    end_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='end_trips'
    )
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(blank=True, null=True)

    pickup_start_dt = models.DateTimeField(blank=True, null=True)
    pickup_end_dt = models.DateTimeField(blank=True, null=True)
    pickup_duration = models.FloatField(default=1.0, help_text="Pickup duration in minutes")  # Default 1 hour

    drop_off_start_dt = models.DateTimeField(blank=True, null=True)
    drop_off_end_dt = models.DateTimeField(blank=True, null=True)
    drop_off_duration = models.FloatField(default=1.0, help_text="Drop-off duration in minutes")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=TripStatus.ONGOING)
    distance = models.FloatField(help_text="Distance in miles")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.id} by {self.driver.name}"


class DriverHos(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='logs')
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='logs')
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
        return f"Rest break for {self.driver_log.driver.name} on {self.driver_log.date}"


# Fueling Model
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
