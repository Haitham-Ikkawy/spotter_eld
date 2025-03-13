from rest_framework import serializers

from spotter_eld.models import Driver, Vehicle, Location, Trip, DriverHos, RestBreak, Fueling


# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


# Vehicle Serializer
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


# Location Serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


# Trip Serializer
class TripSerializer(serializers.ModelSerializer):
    # driver = DriverSerializer()  # Now driver details will be included
    # vehicle = VehicleSerializer()  # Now vehicle details will be included

    class Meta:
        model = Trip
        fields = '__all__'

class TripListSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()  # Now driver details will be included
    vehicle = VehicleSerializer()  # Now vehicle details will be included

    class Meta:
        model = Trip
        fields = '__all__'
# DriverLog Serializer
class DriverLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverHos
        fields = '__all__'


# RestBreak Serializer
class RestBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestBreak
        fields = '__all__'


# Fueling Serializer
class FuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fueling
        fields = '__all__'
