from django.contrib import admin

# Create admin for Vehicle model
from vehicles.models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'model_name',
        'driver',
        'color',
        'registration_number',
        'year_of_manufacture',
    )

admin.site.register(Vehicle, VehicleAdmin)
