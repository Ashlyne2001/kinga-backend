from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    To call this command,

    python manage.py script_runner

    Used to run custom scripts to perform various operations
    """
    help = 'Used to run custom scripts to perform various operations'

    def handle(self, *args, **options):
        pass

        