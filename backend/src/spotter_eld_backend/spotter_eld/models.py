from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Driver(models.Model):
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
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)  # Vehicle Identification Number
    current_mileage = models.IntegerField(default=0)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    start_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='start_trips'
    )
    end_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='end_trips'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    distance = models.FloatField(help_text="Distance in miles")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip {self.id} by {self.driver.name}"

class DriverLog(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='logs')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='logs')
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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(help_text="Duration in hours")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rest break for {self.driver_log.driver.name} on {self.driver_log.date}"

# Fueling Model
class Fueling(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='fuelings')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='fuelings')
    fuel_amount = models.FloatField(help_text="Fuel amount in gallons")
    fuel_cost = models.FloatField(help_text="Fuel cost in dollars")
    mileage_dt_fueling = models.IntegerField(help_text="Mileage at the time of fueling")
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fueling for Trip {self.trip.id} at {self.location.name}"