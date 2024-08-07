
from rest_framework import serializers

from profiles.models import Customer, Driver

class CustomerViewSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CustomerViewSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    full_name = serializers.ReadOnlyField(source='user.get_full_name')
    email = serializers.ReadOnlyField(source='user.email')
    join_date = serializers.SerializerMethodField()
    last_login_date = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'full_name', 
            'email', 
            'phone',
            'current_location_name',
            'current_location_coordinates',
            'join_date', 
            'last_login_date',
        )
        
    def get_join_date(self, obj):
        return obj.get_join_date()
    
    def get_last_login_date(self, obj):
        return obj.get_last_login_date(self.user.get_user_timezone())

    
class DriverViewSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(DriverViewSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    full_name = serializers.ReadOnlyField(source='user.get_full_name')
    email = serializers.ReadOnlyField(source='user.email')
    join_date = serializers.SerializerMethodField()
    last_login_date = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = (
            'full_name', 
            'email', 
            'phone',
            'current_location_name',
            'current_location_coordinates',
            'join_date', 
            'last_login_date',
        )
        
    def get_join_date(self, obj):
        return obj.get_join_date()
    
    def get_last_login_date(self, obj):
        return obj.get_last_login_date(self.user.get_user_timezone())
