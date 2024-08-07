from datetime import datetime, timedelta
from django.conf import settings 

from django.utils import timezone


class DateUtils:
    @staticmethod
    def do_created_dates_compare(date_str, short=False):
        """
        During tests, it's hard to compare dates since the time an object is created
        and when it's evaluated differs slightly or significantly depending on the
        db the test is being ran on. This function just makes sure the datetime 
        provided does not differ by more than an hour from the now time

        date_str ('April, 07, 2021, 10:16:AM')
        """

        preferred_format = settings.PREFERED_DATE_FORMAT2 if short else settings.PREFERED_DATE_FORMAT

        now = timezone.now() + timedelta(hours=3)
        local_date = (now).strftime(preferred_format)

        date1 = datetime.strptime(date_str, preferred_format)
        date2 = datetime.strptime(local_date, preferred_format)

        if (date2 - date1).total_seconds() > 3600:
            return False
        else:
            return True

    @staticmethod
    def do_created_dates_compare2(date_str):
        """
        During tests, it's hard to compare dates since the time an object is created
        and when it's evaluated differs slightly or significantly depending on the
        db the test is being ran on. This function just makes sure the datetime 
        provided does not differ by more than an hour from the now time

        date_str ('April, 07, 2021, 10:16:AM')
        """

        preferred_format = settings.PREFERED_DATE_FORMAT4

        now = timezone.now() + timedelta(hours=3)
        local_date = (now).strftime(preferred_format)

        date1 = datetime.strptime(date_str, preferred_format)
        date2 = datetime.strptime(local_date, preferred_format)

        if (date2 - date1).total_seconds() > 3600:
            return False
        else:
            return True

    @staticmethod
    def do_created_dates_compare_with_format(date_str, date_format):
        """
        During tests, it's hard to compare dates since the time an object is created
        and when it's evaluated differs slightly or significantly depending on the
        db the test is being ran on. This function just makes sure the datetime 
        provided does not differ by more than an hour from the now time

        date_str ('April, 07, 2021, 10:16:AM')
        """
        now = timezone.now() + timedelta(hours=3)
        local_date = (now).strftime(date_format)

        date1 = datetime.strptime(date_str, date_format)
        date2 = datetime.strptime(local_date, date_format)

        if (date2 - date1).total_seconds() > 3600:
            return False
        else:
            return True

    @staticmethod
    def compare_two_datetimes(date1, date2):
        """
        Returns true if the two datetime provide have the same date, hour and 
        minutes. This make it easy to compare 2 datetimes without worrying about
        matching seconds
        """

        date1_str = date1.strftime(settings.PREFERED_DATE_FORMAT)
        date2_str = date2.strftime(settings.PREFERED_DATE_FORMAT)

        return date1_str == date2_str