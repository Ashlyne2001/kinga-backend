from django.contrib import admin

from trips.models import Trip

# Register your models here.
class TripAdmin(admin.ModelAdmin):
    ordering = ('from_location_name',)
    list_display = (
        'from_location_name', 
        'destination_location_name',
        'cost',
        'driver', 
        'customer' 
    )
    fieldsets = []

admin.site.register(Trip, TripAdmin)