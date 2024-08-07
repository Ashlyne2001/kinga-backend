import os

import pytz


from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule

from core.env_checker import EnvironmentChecker

class Command(BaseCommand):
    """
    To call this command,

    python manage.py create_periodic_task
    """
    help = 'Creates periodic tasks'

    def handle(self, *args, **options):

        # Delate all CrontabSchedule and PeriodicTask before creating new ones 
        # to prevent unwanted collisions duplicates
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()
        
        # Only create tasks for production
        

    

  


