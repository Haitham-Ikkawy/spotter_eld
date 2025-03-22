from django.contrib import admin
from .models import Driver, Vehicle, Location, Trip, RestBreak, Fueling

# Register your models here.

# Driver Admin
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'license_number', 'current_cycle_used', 'created_dt', 'updated_dt')
    list_filter = ('created_dt', 'updated_dt')
    search_fields = ('name', 'license_number')
    ordering = ('name',)

# Vehicle Admin
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'year', 'vin', 'current_mileage', 'created_dt', 'updated_dt')
    list_filter = ('name', 'year', 'created_dt')
    search_fields = ('name', 'model', 'vin')
    ordering = ('name', 'model')

# Location Admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude', 'address', 'created_dt', 'updated_dt')
    list_filter = ('created_dt', 'updated_dt')
    search_fields = ('name', 'address')
    ordering = ('name',)

# Trip Admin
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'vehicle', 'start_location', 'end_location', 'start_dt', 'end_dt', 'distance', 'created_dt', 'updated_dt')
    list_filter = ('start_dt', 'end_dt', 'created_dt')
    search_fields = ('driver__name', 'vehicle__name', 'start_location__name', 'end_location__name')
    ordering = ('start_dt',)
#
# # DriverLog Admin
# @admin.register(DriverLog)
# class DriverLogAdmin(admin.ModelAdmin):
#     list_display = ('id', 'driver', 'trip', 'date', 'total_driving_hours', 'total_on_duty_hours', 'created_dt', 'updated_dt')
#     list_filter = ('date', 'created_dt')
#     search_fields = ('driver__name', 'trip__id')
#     ordering = ('date',)

# RestBreak Admin
@admin.register(RestBreak)
class RestBreakAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_dt', 'end_dt', 'duration', 'created_dt', 'updated_dt')
    list_filter = ('start_dt', 'end_dt', 'created_dt')
    search_fields = ('driver_log__driver__name',)
    ordering = ('start_dt',)

# Fueling Admin
@admin.register(Fueling)
class FuelingAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'location', 'amount', 'cost', 'mileage_at_fueling', 'created_dt', 'updated_dt')
    list_filter = ('created_dt', 'updated_dt')
    search_fields = ('trip__id', 'location__name')
    ordering = ('trip__start_dt',)