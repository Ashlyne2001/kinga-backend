from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

from rest_framework import serializers
from accounts.utils.user_type import DRIVER_USER


from profiles.models import Profile

from vehicles.models import Vehicle

class UserSerializer(serializers.ModelSerializer): 
    phone = serializers.IntegerField(required=True,)
    email = serializers.EmailField(
        max_length=30,
        required=True
    )
    password = serializers.CharField(
        min_length=8, 
        max_length=50,
        write_only=True
    )
    current_location_name = serializers.CharField(max_length=30, write_only=True)

    # Vehicle fields
    vehicle_model_name = serializers.CharField(
        max_length=30, 
        write_only=True, 
        required=False
    )
    vehicle_color = serializers.CharField(
        max_length=30, 
        write_only=True, 
        required=False,
    )
    vehicle_registration_number = serializers.CharField(
        max_length=30, 
        write_only=True, 
        required=False,
    )
    vehicle_year_of_manufacture = serializers.IntegerField(
        write_only=True, 
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
            'gender',
            'password',
            'user_type',
            'current_location_name',

            # Vehicle fields
            'vehicle_model_name', 
            'vehicle_color', 
            'vehicle_registration_number', 
            'vehicle_year_of_manufacture'
        )
        
    def create(self, validated_data):
    
        # Use pop to remove these values from validate_data and store them
        # so that we can use them in update the profile
        # user_type = validated_data.pop("user_type")
        current_location_name = validated_data.pop("current_location_name")

        # Vehicle fields
        vehicle_model_name = validated_data.pop("vehicle_model_name", None)
        vehicle_color = validated_data.pop("vehicle_color", None)
        vehicle_registration_number = validated_data.pop("vehicle_registration_number", None)
        vehicle_year_of_manufacture = validated_data.pop("vehicle_year_of_manufacture", None)
        
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Save location data
        if user.user_type == DRIVER_USER:
            user.driver.current_location_name = current_location_name
        else:
            user.customer.current_location_name = current_location_name

        # Create Vehicle
        if user.user_type == DRIVER_USER and vehicle_model_name:
            Vehicle.objects.create(
                driver=user.driver,
                model_name=vehicle_model_name,
                color=vehicle_color,
                registration_number=vehicle_registration_number,
                year_of_manufacture=vehicle_year_of_manufacture,
            )

        return user
    
