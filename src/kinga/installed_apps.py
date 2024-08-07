# Since we have 3 different settings for our 3 envs, this will provide a 
# central place for common installed apps

'''
Inchoroi
Entiyani 
Kiremisho 


'''


# Application definition
INSTALLED_APPS = [
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mysettings.apps.MysettingsConfig',
    'accounts.apps.AccountsConfig',
    'profiles.apps.ProfilesConfig',
    'trips.apps.TripsConfig',
    'vehicles.apps.VehiclesConfig',
    
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'api.apps.ApiConfig',
    
    'channels',
    "debug_toolbar",

    'corsheaders',
    'django_celery_beat'
]