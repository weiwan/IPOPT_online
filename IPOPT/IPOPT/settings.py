"""
Django settings for IPOPT project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from mongoengine import connect
from os.path import join, dirname
import redis


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n_eda=3e+=$%&v_3ux&su1#f2^@&kro7fx$)p$ewmk2@i9@x&u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
    )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mongoengine.django.mongo_auth',
    'django_gravatar',
    'submission',
    'accounts',
    'mongonaut',
    'discussion',
    'analysis',
    'notification',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'IPOPT.urls'

WSGI_APPLICATION = 'IPOPT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
AUTH_USER_MODEL = 'mongo_auth.MongoUser'

SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/ipopt/static'
TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates/'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# MONGODB_HOST = "ec2-174-129-116-133.compute-1.amazonaws.com"
# MONGODB_HOST = '107.21.222.181'
MONGODB_HOST = '127.0.0.1'
MONGODB_USER = 'django'
MONGODB_PWD = 'mongodb15637finalproject'
# MONGODB_HOST = "ec2-54-147-197-250.compute-1.amazonaws.com"
# IPOPT_HOST = "ec2-54-147-197-250.compute-1.amazonaws.com"

# MONGODB_HOST = "107.21.222.181"
IPOPT_HOST = "54.174.175.187"
IPOPT_PORT = 8080
# connect('IPOPT', host=MONGODB_HOST, port=27017, username=MONGODB_USER, password=MONGODB_PWD)
connect('IPOPT', host=MONGODB_HOST, port=27017)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ipoptcmu@gmail.com'
EMAIL_HOST_PASSWORD = '12332112345677654321'
EMAIL_PORT = 587


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/submit'
REGISTER_REDIRECT_URL = '/accounts/activate/'

# ALLOWED_HOSTS = ['192.168.10.10',]