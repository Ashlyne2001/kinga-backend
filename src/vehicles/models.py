from django.db import models

from profiles.models import Driver

# Create your models here.
class Vehicle(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    model_name = models.CharField(
        verbose_name='model name',
        default='',
        max_length=50,
    )
    color = models.CharField(
        verbose_name='from location name',
        default='',
        max_length=50,
    )
    registration_number = models.CharField(
        verbose_name='registration number',
        default='',
        max_length=50,
    )
    year_of_manufacture = models.BigIntegerField(
        verbose_name='year of manufacture',
        default=0,
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        db_index=True,
        default=0,
    )

    def __str__(self) -> str:
        return str(self.model_name)

    def save(self, *args, **kwargs):

        # If reg_no is 0 get a unique one
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel

            self.reg_no = GetUniqueRegNoForModel(self.__class__)

        super(Vehicle, self).save(*args, **kwargs)