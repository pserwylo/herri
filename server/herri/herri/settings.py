"""
Django settings for herri project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# This should be setup in local_settings.py instead of here. 
# That way, database credentials will not make it into version control. 
# SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
# These should probably be changed in your local_settings.py if you are
# interested in changing them.
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'api',
	'web',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
#	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'herri.urls'

WSGI_APPLICATION = 'herri.wsgi.application'


# Database
# This should be setup in local_settings.py instead of here. 
# That way, database credentials will not make it into version control. 
# DATABASES = {}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SERIALIZATION_MODULES = {
	'json': 'wadofstuff.django.serializers.json'
}

STATIC_ROOT = '/opt/herri-static'

# Now import settings which were not stored in version control...
# http://stackoverflow.com/a/5583253
try:
    from local_settings import *
except ImportError:
    pass
