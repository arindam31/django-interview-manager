"""
Django settings for TheEvaluator project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+m5kfxu4@uuzymgw8sx1@cpse*pqfd1%(0o(r_ms=+fud-#xi9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [


    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'mathfilters',
    'Evaluator',
    'django.contrib.admin', # This ordering has been brought
    'django.contrib.auth', # down so that custom auth templates works
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'Recruitment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Recruitment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# This is the url after one logs in.
LOGIN_REDIRECT_URL = '/profile'

# This is where one would be lead if not logged in.
LOGIN_URL = '/login'

#Logging Settings
LOG_LOCATION = os.path.join(BASE_DIR, 'Logs')

LOGGING = {
    'version':1,
    'disable_existing_loggers': True,
    'formatters':{
        'my_formatter':{
                        'format': '%(asctime)s, File: %(module)s.py, Function: %(funcName)s, Message: %(message)s'
                    }

                },
    'handlers':{
        'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(LOG_LOCATION, 'debug.log'),
                    'formatter': 'my_formatter',
                },
        'errorfile': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(LOG_LOCATION, 'error.log'),
                    'formatter': 'my_formatter',
                },
        'mail_admins': {
                    'level': 'ERROR',
                    'class': 'django.utils.log.AdminEmailHandler',
                    'include_html': False,
                },
        'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'my_formatter',
                },
               },
    'loggers': {

            'mylogs': {
                        'handlers': ['file'],
                        'level': 'DEBUG',
                        'propagate': True,
                      },
            'django': {
                'handlers': ['errorfile'],
                'level': 'ERROR',
                'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
                }
            }

