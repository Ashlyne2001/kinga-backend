import datetime
import os
import pytz
import dateutil.parser

from django.utils import timezone
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinga_cloud.settings')

def utc_to_local_datetime(utc_time, local_timezone=settings.LOCATION_TIMEZONE):
    """
    Args:
        utc_time (datetime.datetime) - Utc datetime to convert
        local_timezone (str) - A string representing the chosen Django's timezone

    Returns:
        (datetime.datetime) - A local datetime
    """
    return utc_time.astimezone(pytz.timezone(local_timezone))

def utc_to_local_datetime_with_format(utc_time, local_timezone, short=False):

    # Change time from utc to local
    date = utc_to_local_datetime(utc_time, local_timezone)

    # Change date format
    local_date_and_time = (date).strftime(
        settings.PREFERED_DATE_FORMAT2 if short else settings.PREFERED_DATE_FORMAT
    )

    return local_date_and_time

def utc_to_local_datetime_with_number_format(utc_time, local_timezone):

    # Change time from utc to local
    date = utc_to_local_datetime(utc_time, local_timezone)

    # Change date format
    local_date_and_time = (date).strftime(settings.PREFERED_DATE_FORMAT4)

    return local_date_and_time

def utc_to_local_datetime_with_date_format(utc_time, local_timezone):

    # Change time from utc to local
    date = utc_to_local_datetime(utc_time, local_timezone)

    # Change date format
    local_date_and_time = (date).strftime(settings.PREFERED_DATE_FORMAT3)

    return local_date_and_time





def iso_date_str_to_local_datetime(str_date, local_timezone, time_rep=datetime.time.min):
    """
    Accepts a date in iso format and then returns it as a datetime.datetime in
    the local timezone
    """
    
    try:

        my_date = datetime.date.fromisoformat(str_date)

        return utc_to_local_datetime(
            datetime.datetime.combine(my_date, time_rep),
            local_timezone
        )
    
    except: # pylint: disable=bare-except
        return None

def iso_date_str_to_local_datetime2(str_date, local_timezone, time_rep=datetime.time.min):
    """
    Accepts a date in iso format and then returns it as a datetime.datetime in
    the local timezone
    """
    
    try:

        my_date = datetime.date.fromisoformat(str_date)

        return utc_to_local_datetime(
            datetime.datetime.combine(my_date, time_rep),
            local_timezone
        )
    
    except: # pylint: disable=bare-except
        return None

def date_to_local_datetime(date, local_timezone, time_rep=datetime.time.min):
    """
    Accepts a date in iso format and then returns it as a datetime.datetime in
    the local timezone
    """

    my_date = datetime.date.fromtimestamp(date.timestamp())

    return utc_to_local_datetime(
        datetime.datetime.combine(my_date, time_rep),
        local_timezone
    )



def is_valid_iso_format(str_date):
    """
    Returns true if str date is in correct iso format and false otherwise
    """
    try:

        datetime.date.fromisoformat(str_date)

        return True

    except: # pylint: disable=bare-except
        return False


class DateAndTimeHelpers:

    @staticmethod
    def make_date_local_timezone_aware(given_datetime):
        """
        Args:
            given_datetime (datetime.datetime): Datetime to be convereted into
            local timezone

        Returns:
            datetime.datetime: In local timezone
        """

        return timezone.make_aware(
            value=given_datetime,
            timezone=pytz.timezone(settings.LOCATION_TIMEZONE)
        )

    @staticmethod
    def get_timenow_for_appsheet():
        """
        Returns now time in a format suitable for appsheet

        Example return:
            3/13/2022 3:46:00
        """
        date = utc_to_local_datetime(utc_time=timezone.now())

        # Change date format
        return (date).strftime("%-m/%-d/%Y %-I:%M:00")

    @staticmethod
    def is_iso_date_bigger_or_equal_to_date(iso_date, compare_date):
        
        iso_date_datetime = dateutil.parser.isoparse(iso_date)

        return iso_date_datetime >= compare_date

    @staticmethod
    def date_to_iso_format(date):
        """
        Args:
            date (Datetime) - Date to be converted

        Returns:
            str - Date in iso format string E.g 2020-03-30T18:30:00.000Z
        """
        return (date).strftime("%Y-%m-%dT00:00:00.000Z")

    @staticmethod
    def date_to_simple_number_format(utc_date, local_timezone=None):

        if local_timezone:
            
            # Change time from utc to local
            date = utc_to_local_datetime(utc_date, local_timezone)

            # Change date format
            local_date_and_time = (date).strftime(settings.PREFERED_DATE_FORMAT5)

            return local_date_and_time

        else:
            return (utc_date).strftime(settings.PREFERED_DATE_FORMAT5)

    @staticmethod
    def utc_to_local_datetime_with_format(
        utc_time, 
        date_format, 
        local_timezone=settings.LOCATION_TIMEZONE):

        # Change time from utc to local
        date = utc_to_local_datetime(utc_time, local_timezone)

        # Change date format
        local_date_and_time = (date).strftime(date_format)

        return local_date_and_time

    @staticmethod
    def date_to_min_or_max(date, time_rep=datetime.time.min):
        """
        Converts the provided date into it's max or min  

        Args:
            date (Datetime) - Date to be converted to it's max or min
            time_rep (time.min or time.max)  

        Returns:
            An aware max or min datetime 
        """

        my_date = datetime.date.fromtimestamp(date.timestamp())

        return timezone.make_aware(datetime.datetime.combine(my_date, time_rep))

    @staticmethod
    def get_min_and_max_date(start_date, end_date):
        """
        Converts the start date to the minimum date and end date to the maximum 
        date.

        Returns: 
            Tuple of min and max date from the given start date and end date
        """

        min_date = DateAndTimeHelpers.date_to_min_or_max(
            start_date,
            datetime.time.min
        )
     
        max_date = DateAndTimeHelpers.date_to_min_or_max(
            end_date,
            datetime.time.max
        )
        

        return min_date, max_date

    @staticmethod
    def get_local_min_and_max_date(start_date, end_date):
        """
        Converts the start date to the local minimum date and end date to the 
        local maximum date.

        Returns: 
            Tuple of min and max date from the given start date and end date
        """
        local_min_date = DateAndTimeHelpers.make_date_local_timezone_aware(
            given_datetime=DateAndTimeHelpers.date_to_min_or_max(
                start_date,
                datetime.time.min
            )
        )

        local_max_date = DateAndTimeHelpers.make_date_local_timezone_aware(
            given_datetime=DateAndTimeHelpers.date_to_min_or_max(
                end_date,
                datetime.time.max
            )
        )

        return local_min_date, local_max_date

    @staticmethod
    def get_utc_and_local_tz_diff():
        """
        Returns the difference in hours between utc timezone and local timezone
        """

        today_date = datetime.datetime.now()

        utc_tz = pytz.timezone('UTC')
        local_tz = pytz.timezone(settings.LOCATION_TIMEZONE)
        
        return (utc_tz.localize(today_date) - 
                local_tz.localize(today_date).astimezone(utc_tz))\
                .seconds/3600
            
