"""
Django settings for kinga project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
# pylint: disable=wildcard-import

import os

from .installed_apps import*

#from celery.schedules import crontab

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^ixl)t^__(2r6ycl@t1p@-xzc253o83820m^$4f$g!90$ao=-f'


# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
# http://e108a8a0.ngrok.io/ 

#ALLOWED_HOSTS = ['127.0.0.1', '10.0.2.2', 'ws.mtq.origin.socket.host', '721d2b02.ngrok.io']
ALLOWED_HOSTS = ['*']

# Application definition has been moved to installed_apps.py for easier common
# installed apps access# Application definition has been moved to installed_apps.py

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kinga_dev',
        'USER': 'webapp',
        'PASSWORD': 'qXKkn945ZCa4SWTUddK3',
        'HOST': 'aegeus.c1q9l5pgadky.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
'''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = ()

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
TESTING_MEDIA_ROOT = MEDIA_ROOT + '/images/tests/'



#---------------- Celery Settings --------------------------------------
REDIS_PORT = 6379
REDIS_URL = f'redis://localhost:{REDIS_PORT}'

# CELERY STUFF
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
#---------------- End Celery Settings --------------------------------------

#---------------- Channel Settings --------------------------------------
ASGI_APPLICATION = "kinga.asgi.application"
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_URL)]
        },
    },
}
#---------------- End Channel Settings --------------------------------------
