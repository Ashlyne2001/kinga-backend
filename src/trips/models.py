from django.db import models
from django.utils import timezone
from django.conf import settings

from core.time_utils.time_localizers import utc_to_local_datetime_with_format
from profiles.models import Customer, Driver

# Create your models here.
class Trip(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # Locations names
    from_location_name = models.CharField(
        verbose_name='from location name',
        default='',
        max_length=50,
    )
    destination_location_name = models.CharField(
        verbose_name='destination location name',
        default='',
        max_length=50,
    )

    # Locations coordinates
    from_location_coordinates = models.JSONField(
        verbose_name='from location coordinates', 
        default=dict,
        blank=True,
        null=True
    )
    destination_location_coordinates = models.JSONField(
        verbose_name='destination location coordinates', 
        default=dict,
        blank=True,
        null=True
    )
    start_time = models.DateTimeField(
        verbose_name='start time',
        default=timezone.now,
        db_index=True,
    )
    end_time = models.DateTimeField(
        verbose_name='end time',
        default=timezone.now,
        db_index=True,
    )
    is_completed = models.BooleanField(   
        verbose_name='is completed',
        default=False,
    )
    cost = models.DecimalField(
        verbose_name='cost',
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        # unique=True,
        db_index=True,
        default=0,
    )

    def __str__(self) -> str:
        return str(f'{self.from_location_name} - {self.destination_location_name}')
    
    def get_driver_name(self):
        return self.driver.user.get_full_name() if self.driver else ''
    
    def get_customer_name(self):
        return self.customer.user.get_full_name() if self.customer else ''

    def get_start_time(self):
        """Return the start time in local time format (July, 06, 2022, 10:57:AM)"""
        return utc_to_local_datetime_with_format(
            self.start_time, 
            settings.LOCATION_TIMEZONE
        )

    def get_end_time(self):
        """Return the end time in local time format (July, 06, 2022, 10:57:AM)"""
        return utc_to_local_datetime_with_format(
            self.end_time, 
            settings.LOCATION_TIMEZONE
        )
    
    def get_trip_duration(self):
        """Return the trip duration in minutes"""
        minutes = (self.end_time - self.start_time).total_seconds() / 60

        return f'{round(minutes, 2)} minutes'
    
    def get_trip_cost(self):
        """Return the trip cost in KES"""
        return f'Ksh {self.cost}'

    def save(self, *args, **kwargs):

        # If reg_no is 0 get a unique one
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel

            self.reg_no = GetUniqueRegNoForModel(self.__class__)

        super(Trip, self).save(*args, **kwargs)