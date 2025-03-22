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
    start_location = LocationSerializer()  # Now driver details will be included
    end_location = LocationSerializer()  # Now driver details will be included
    driver = DriverSerializer()  # Now driver details will be included
    vehicle = VehicleSerializer()  # Now vehicle details will be included
    show_start_pickup = serializers.SerializerMethodField()
    show_end_pickup = serializers.SerializerMethodField()
    show_start_drop_off = serializers.SerializerMethodField()
    show_end_drop_off = serializers.SerializerMethodField()
    extra_fields = ['show_start_pickup', 'show_end_pickup', 'show_start_drop_off', 'show_end_drop_off']

    def get_show_start_pickup(self, obj):
        """Show End Pickup if trip is started but neither Start Dropoff nor End Dropoff exists."""
        return bool(obj.start_dt and (not obj.pickup_start_dt and not obj.pickup_end_dt and not obj.end_dt))

    def get_show_end_pickup(self, obj):
        """Show End Pickup if trip is started but neither Start Dropoff nor End Dropoff exists."""
        return bool(obj.start_dt and obj.pickup_start_dt and (not obj.pickup_end_dt and not obj.end_dt))

    def get_show_start_drop_off(self, obj):
        """Show Start Dropoff if trip has start_dt and End Pickup exists but no End Dropoff."""
        # return bool(obj.start_dt and obj.pickup_end_dt and not obj.end_dt)

        return bool(obj.start_dt and obj.pickup_start_dt and obj.pickup_end_dt and (not obj.drop_off_start_dt and not obj.drop_off_end_dt and not obj.end_dt))

    def get_show_end_drop_off(self, obj):
        """Show End Dropoff if trip has End Pickup and Start Dropoff."""
        # return bool(obj.pickup_end_dt and obj.end_dt)

        return bool(obj.start_dt and obj.drop_off_start_dt and (not obj.drop_off_end_dt and not obj.end_dt))

    class Meta:
        model = Trip
        fields = '__all__'


# DriverLog Serializer
class DriverLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverHos
        fields = '__all__'


# RestBreak Serializer


class RestBreakListSerializer(serializers.ModelSerializer):
    trip = TripSerializer()
    location = LocationSerializer()

    class Meta:
        model = RestBreak
        fields = '__all__'


class RestBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestBreak
        fields = '__all__'


# Fueling Serializer
class FuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fueling
        fields = '__all__'


# Fueling Serializer
class FuelingListSerializer(serializers.ModelSerializer):
    trip = TripSerializer()
    location = LocationSerializer()

    class Meta:
        model = Fueling
        fields = '__all__'


class TripActionSerializer(serializers.Serializer):
    type = serializers.CharField()
    _dt = serializers.DateTimeField()
    location = serializers.CharField()
    duration = serializers.IntegerField(required=False, allow_null=True)


# class TripSerializer(serializers.ModelSerializer):
#     actions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Trip
#         fields = ['id', 'driver', 'actions']
#
#     def get_actions(self, obj):
#         actions = []
#
#         # Trip Start
#         actions.append({
#             "type": "Trip Start",
#             "_dt": obj.start_dt,
#             "location": obj.start_location,
#             "duration": None
#         })
#
#         # Rest Breaks
#         for break_obj in obj.rest_breaks.all():
#             actions.append({
#                 "type": "Rest Break",
#                 "_dt": break_obj.break_dt,
#                 "location": break_obj.location,
#                 "duration": break_obj.duration_minutes
#             })
#
#         # Fuelings
#         for fueling in obj.fuelings.all():
#             actions.append({
#                 "type": "Fueling",
#                 "_dt": fueling.fueling_dt,
#                 "location": fueling.location,
#                 "duration": fueling.duration_minutes
#             })
#
#         # Trip End
#         if obj.end_dt:
#             actions.append({
#                 "type": "Trip End",
#                 "_dt": obj.end_dt,
#                 "location": obj.end_location,
#                 "duration": None
#             })
#
#         # Sort actions by datetime (_dt)
#         actions = sorted(actions, key=lambda x: x["_dt"])
#         return actions