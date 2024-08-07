
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from .utils.create_users import create_app_initial_users 

User = get_user_model()

class Command(BaseCommand):
    """
    To call this command,
    
    python manage.py create_app_users
    
    """
    help = 'Creates test data'
  
    def handle(self, *args, **options):

        create_app_initial_users()

        self.stdout.write(self.style.SUCCESS('Successfully prepaired sample data')) 
        
        