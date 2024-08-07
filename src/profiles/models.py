import os

from django.db import models
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.utils.validators import validate_phone_for_models
from core.time_utils.time_localizers import utc_to_local_datetime_with_format

# Create your models here.

# Profile image directory


def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/profiles/<profiile.reg_no>_<filename>.jpg

    path = '{}{}_{}'.format(
        settings.IMAGE_SETTINGS['profile_images_dir'], instance.reg_no, filename)

    return path

# Receipt image directory


def receipt_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/receipts/<receipt.reg_no>_<filename>.jpg

    path = '{}{}_{}'.format(
        settings.IMAGE_SETTINGS['receipt_images_dir'], instance.reg_no, filename)

    return path


class CommonProfileMethodsMixin:
    """
    This mixin should only contain universal methods that can be used by both the
    Profile and EmployeeProfile models without causing any problems or security flaws
    """

    def __str__(self):
        return self.user.email

    def get_short_name(self):
        """Return the user name"""
        return self.user.get_short_name()

    def get_full_name(self):
        """Return the user full name"""

        full_name = ""
        with transaction.atomic():
            full_name = self.user.get_full_name()

        return full_name

    def get_join_date(self, local_timezone):
        """Return the user join date in local time format"""
        return utc_to_local_datetime_with_format(self.join_date, local_timezone)
    # Make join_date to be filterable
    get_join_date.admin_order_field = 'join_date'

    # TODO Test this
    def get_admin_join_date(self):
        """Return the join date in local time format"""
        return self.get_join_date(settings.LOCATION_TIMEZONE)
    # Make join_date to be filterable
    get_admin_join_date.admin_order_field = 'join_date'

    def get_last_login_date(self, local_timezone):
        """Return the user last login date in local time format"""

        """ 
        If the profile has never logged in, getting date will fail and so
        we return False
        """
        try:

            # Change time from utc to local
            local_last_login_date = utc_to_local_datetime_with_format(
                self.user.last_login,
                local_timezone
            )

        # pylint: disable=bare-except
        except:
            local_last_login_date = False

        return local_last_login_date
    # Make last_login to be filterable
    get_last_login_date.admin_order_field = 'last_login'

    # TODO Test this
    def get_admin_last_login_date(self):
        """Return the user last login date in local time format"""
        return self.get_last_login_date(settings.LOCATION_TIMEZONE)
    # Make last_login to be filterable
    get_admin_last_login_date.admin_order_field = 'last_login'

    def get_profile_image_url(self):
        """
        Return image url or an empty string
        """
        try:
            return self.image.url

        # pylint: disable=bare-except
        except:
            return ""

    def get_location(self):
        """
        Return location or return "Not set" if location is not there
        """

        if self.location:
            return self.location
        else:
            return "Not set"
        
    def mark_staff_as_approved(self):
        """ 
        If user is staff mark profile as approved
        """
        if self.user.is_staff:
            self.approved = True

    def sync_profile_phone_and_its_user_phone(self):
        """
        Make sure user's phone is the same with profile's phone
        """

        user = self.user

        if not self.phone == user.phone:
            user.phone = self.phone
            user.save()

    def profile_image_cleanup(self):
        """
        This function does the following assignments
        1. When profile has no image, the no image image is attached to the profile
        2. Delets old profile images when new ones are uploaded.
        """

        # This is just a precaution
        if not self.image:
            self.image = settings.IMAGE_SETTINGS['no_image_url']

        if not self.old_image:
            self.old_image = self.image

        # Delele old_image if profile has a new image
        if self.old_image:
            # Check if old image and current image are the same
            if not self.old_image == self.image:

                # Only delete images that are in the profiles image path to avoid
                # deleting important images
                if '/images/profiles/' in self.old_image.path:

                    # Try deleting the old_image's image file
                    try:
                        os.remove(self.old_image.path)

                    # pylint: disable=bare-except
                    except:
                        pass

                # Assign old_image with a new image path
                self.old_image = self.image


# ========================== START Profile Models

class Profile(CommonProfileMethodsMixin, models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=profile_directory_path,
        default=settings.IMAGE_SETTINGS['no_image_url'],
        verbose_name='image',
    )
    old_image = models.ImageField(
        default=settings.IMAGE_SETTINGS['no_image_url'],
        verbose_name='old image',
    )
    phone = models.BigIntegerField(
        verbose_name='phone',
        validators=[validate_phone_for_models],
        unique=True,
        default=0
    )
    approved = models.BooleanField(
        verbose_name='approved',
        default=False)  # Consider deletion
    join_date = models.DateTimeField(
        verbose_name='join date',
        default=timezone.now,
        db_index=True)
    business_name = models.CharField(
        verbose_name='business name',
        max_length=60,
        default=''
    )
    location = models.CharField(
        verbose_name='location',
        max_length=100,
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        db_index=True,
        default=0,
        editable=False
    )

    """ The CommonProfileMethodsMixin defines the following methods
    
    __str__
    get_short_name
    get_full_name
    get_join_date
    get_last_login_date
    get_profile_image_url
    get_location
    mark_staff_as_approved
    sync_profile_phone_and_its_user_phone
    profile_image_cleanup
    """
    def save(self, *args, **kwargs):

        # Sync User's and profile phone
        self.sync_profile_phone_and_its_user_phone()

        # Deletes old profile images when new ones are uploaded
        self.profile_image_cleanup()

        # If user is staff mark profile as approved
        self.mark_staff_as_approved()

        # If user is staff mark profile as approved
        if self.user.is_staff:
            self.approved = True

        """ Only Save when the user is an top user """
        # if self.user.user_type == ADMIN_USER:

        # Call the "real" save() method.
        super(Profile, self).save(*args, **kwargs)

class Driver(CommonProfileMethodsMixin, models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        verbose_name='phone',
        default='',
        max_length=20,
        blank=True,
    )
    current_location_name = models.CharField(
        verbose_name='current location name',
        default='',
        max_length=50,
    )
    current_location_coordinates = models.JSONField(
        verbose_name='current location coordinates', 
        default=dict,
        blank=True,
        null=True
    )
    join_date = models.DateTimeField(
        verbose_name='join date',
        default=timezone.now,
        db_index=True,
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        # unique=True,
        db_index=True,
        default=0,
    )

   
    def get_join_date(self):
        """Return the join date in local time format (July, 06, 2022, 10:57:AM)"""
        return utc_to_local_datetime_with_format(
            self.join_date, 
            settings.LOCATION_TIMEZONE
        )

    def get_number_of_trips(self):
        return self.trip_set.all().count()

    def save(self, *args, **kwargs):

        self.phone = self.phone if self.phone else ''

        # If reg_no is 0 get a unique one
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel

            self.reg_no = GetUniqueRegNoForModel(self.__class__)

        super(Driver, self).save(*args, **kwargs)


class Customer(CommonProfileMethodsMixin, models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        verbose_name='phone',
        default='',
        max_length=20,
    )
    current_location_name = models.CharField(
        verbose_name='current location name',
        default='',
        max_length=50,
    )
    current_location_coordinates = models.JSONField(
        verbose_name='current location coordinates', 
        default=dict,
        blank=True,
        null=True
    )
    join_date = models.DateTimeField(
        verbose_name='join date',
        default=timezone.now,
        db_index=True,
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        default=0,
        db_index=True
    )

    def get_join_date(self):
        """Return the join date in local time format (July, 06, 2022, 10:57:AM)"""
        return utc_to_local_datetime_with_format(
            self.join_date, 
            settings.LOCATION_TIMEZONE
        )

    def get_number_of_trips(self):
        return self.trip_set.all().count()

    def save(self, *args, **kwargs):

        self.phone = self.phone if self.phone else ''

        # If reg_no is 0 get a unique one
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel

            self.reg_no = GetUniqueRegNoForModel(self.__class__)

        super(Customer, self).save(*args, **kwargs)