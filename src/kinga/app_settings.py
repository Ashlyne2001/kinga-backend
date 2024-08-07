import datetime
from decimal import Decimal
import os
import sys
import pytz

from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "django_cprofile_middleware.middleware.ProfilerMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'kinga.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kinga.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# APPEND_SLASH=False

# Internationalization 'Africa/Nairobi'
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Nairobi'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# User settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.User'

# ---------------- Logging Settings --------------------------------------
APP_NAME = 'kinga_backend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s kinga_backend %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'page_views_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './xlogs/page_views.log',
            'formatter': 'simple'
        },
        'test_page_views_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './xlogs/test_page_views.log',
            'formatter': 'simple'
        },
        'page_critical_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './xlogs/page_critical.log',
            'formatter': 'simple'
        },
        'test_page_critical_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './xlogs/test_page_critical.log',
            'formatter': 'simple'
        },

        'software_task_critical_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './xlogs/software_task_critical.log',
            'formatter': 'simple'
        },
        'test_software_task_critical_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './xlogs/test_software_task_critical.log',
            'formatter': 'simple'
        },

        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'page_views_logger': {
            'handlers': ['page_views_logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'page_critical_logger': {
            'handlers': ['page_critical_logfile'],
            'level': 'ERROR',
            'propagate': True,
        },

        'test_page_views_logger': {
            'handlers': ['test_page_views_logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'test_page_critical_logger': {
            'handlers': ['test_page_critical_logfile'],
            'level': 'ERROR',
            'propagate': False,
        },

        'software_task_critical_logger': {
            'handlers': ['software_task_critical_logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'test_software_task_critical_logger': {
            'handlers': ['test_software_task_critical_logfile',],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Enable papertail when in production only
if int(os.environ.get("WE_IN_CLOUD", default=0)):

    LOGGING['handlers'].update( 
        {
            'SysLog': {
                'level': 'INFO',
                'class': 'logging.handlers.SysLogHandler',                                                    
                'formatter': 'simple',
                'address': ('logs.papertrailapp.com', 45047)                                                 
            },
        }
    )

    LOGGING['loggers'].update(
        {
            'page_views_logger': {
                'handlers': ['page_views_logfile', 'SysLog'],
                'level': 'INFO',
                'propagate': True,
            },
            'software_task_critical_logger': {
                'handlers': ['software_task_critical_logfile', 'SysLog'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    )


# ---------------- End Logging Settings -----------------------------------


# ---------------- Cache Settings --------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
# ---------------- End Cache Settings --------------------------------------

""" ****************** Django toolbar Start ****************** """

INTERNAL_IPS = ['127.0.0.1']
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

""" ****************** Django toolbar End ****************** """

""" ****************** Business Data Start ****************** """
PROD_URL = 'https://kinga.obriate.com'

""" ****************** Business Data Start End ****************** """


""" ****************** Images Start ****************** """
IMAGE_SETTINGS = {
    'no_image_url': 'images/no_image.jpg',
    'profile_images_dir': 'images/profiles/',
    'product_images_dir': 'images/products/',
    'receipt_images_dir': 'images/receipts/'
}

""" ****************** Images End ****************** """


""" ********************************* Mpesa End ************************************ """

""" ****************** Equity Start ****************** """

""" ********************************* Equity End ************************************ """

""" ****************** Timezone  Start ****************** """
LOCATION_TIMEZONE = 'Africa/Nairobi'
PREFERED_DATE_FORMAT = "%B, %d, %Y, %I:%M:%p" # September, 23, 2022, 12:00:AM
PREFERED_DATE_FORMAT2 = "%b, %d, %Y, %I:%M:%p" # Sep, 23, 2022, 12:00:AM
PREFERED_DATE_FORMAT3 = "%B, %d, %Y" # September, 23, 2022
PREFERED_DATE_FORMAT4 = "%Y-%m-%d" # 2022-09-23
PREFERED_DATE_FORMAT5 = "%d/%m/%Y" # 23/09/2022
PREFERED_DATE_FORMAT6 = "%d %B %Y" 
PREFERED_DATE_FORMAT7 = "%d %b %Y" # 23 September 2022
DEFAULT_START_DATE = timezone.make_aware(
    value=datetime.datetime(1970, 1, 1), 
    timezone=pytz.utc
)
""" ****************** Timezone End ****************** """

MY_SITE_URL = 'http://127.0.0.1:8000'

WE_IN_CLOUD = int(os.environ.get("WE_IN_CLOUD", default=0))

# ---------------- REST password Settings --------------------------------------

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 24


if WE_IN_CLOUD:
    FRONTEND_SITE_NAME = 'https://portal.kinga.com/'
else:
    FRONTEND_SITE_NAME = 'http://localhost:4200'

# ---------------- End REST password Settings --------------------------------------

""" ********************************* My Throttle Start ********************************* """
# TODO For testing reasons, we increase throttle limits but we should change them
# befor going live
THROTTLE_RATES = {
    'login_rate': '10/m',
    'api_token_rate': '10/m',
}

DEBUG = int(os.environ.get("DEBUG", default=0))
TESTING_MODE = sys.argv[1:2] == ['test']
WE_IN_CLOUD = int(os.environ.get("WE_IN_CLOUD", default=0))
WE_IN_DOCKER = int(os.environ.get("WE_IN_DOCKER", default=0))

""" ******************** Global Email Settings Start ******************** """

# if WE_IN_CLOUD:
if WE_IN_CLOUD or WE_IN_DOCKER :
    # Email Backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True

else:
    EMAIL_HOST_USER ='webmaster@localhost'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_ERROR_REPORTING_ADDRESS = 'ashlyneokumu@gmail.com'
EMAIL_HEADERS = {'From': 'kinga <info@kinga.com>'}

""" ******************** Global Email Settings End ******************** """\

PYTHON_REQUESTS_TIMEOUT = 60 # 10 Seconds

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    
    'https://*.obriate.com',
]
