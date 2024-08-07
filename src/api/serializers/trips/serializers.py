
from rest_framework import serializers

from trips.models import Trip

class TripListSerializer(serializers.ModelSerializer):

    driver_name = serializers.ReadOnlyField(source='driver.user.get_full_name')
    customer_name = serializers.ReadOnlyField(source='customer.user.get_full_name')
    start_time = serializers.ReadOnlyField(source='get_start_time')
    end_time = serializers.ReadOnlyField(source='get_end_time')
    duration = serializers.ReadOnlyField(source='get_duration')
    cost = serializers.ReadOnlyField(source='get_trip_cost')

    class Meta:
        model = Trip
        fields = (
            'driver_name',
            'customer_name',
            'from_location_name',
            'destination_location_name',
            'from_location_coordinates',
            'destination_location_coordinates',
            'start_time',
            'end_time',
            'duration',
            'cost',
            'is_completed',
            'reg_no'
        )
            
        
