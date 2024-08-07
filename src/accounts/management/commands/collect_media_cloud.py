import os
from os import listdir
from os.path import isfile, join

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage

class CollectMediaFiles:

    def __init__(self):
        self.original_assets_dir = './accounts/management/commands/utils/createmedia_assets/'
        self.target_dir = f'.{settings.MEDIA_URL}'

        # Copy media
        self.copy_media_from_folder()

    def copy_files(self, target_dir):
        if not self.assest_dir_exists(target_dir):
            raise Exception(f"Cannot seem to find {target_dir}")

        self.copy_directory_assets(target_dir)

    def copy_media_from_folder(self):

        # Copy media files
        self.copy_files('images/')
        self.copy_files('images/profiles/')

        self.copy_files('images/tests/')
        self.copy_files('images/tests/images/profiles/')
  
    def copy_directory_assets(self, path):
        # Copy items in assets_dir into bucket's path

        assets_dir = f'{self.original_assets_dir}{path}'

        files = [assets_dir + f for f in listdir(assets_dir) if isfile(join(assets_dir, f))]

        for f in files:
            
            file = open(f, 'rb')
            file_target_dir = f'{path}{os.path.basename(file.name)}'

            print('>>>>> ', file_target_dir)

            if not default_storage.exists(file_target_dir):
                default_storage.save(file_target_dir, file)    
    
    def assest_dir_exists(self, path):

        assets_dir = f'{self.original_assets_dir}{path}'

        if os.path.exists(assets_dir):
            return True
        else:
            return False
 
class Command(BaseCommand):
    """
    To call this command,
    
    python manage.py collect_media_cloud
    
    Used to create neccessarry folders and image files in the cloud media folder
    """
    help = 'Used to prepare media folder'

    def handle(self, *args, **options):

        CollectMediaFiles()

        self.stdout.write(self.style.SUCCESS('Media files collected successfully')) 