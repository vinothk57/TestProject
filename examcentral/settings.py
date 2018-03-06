"""
Django settings for examcentral project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import examcentralapp
examcentralapppath = os.path.dirname(examcentralapp.__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_)e(5(i_b+8!-%oln2k-e&js@na&-ft%p$kz^d8o6%4t7$avak'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['13.126.104.9', 'quizbuzz.in']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'examcentralapp',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'examcentral.urls'

WSGI_APPLICATION = 'examcentral.wsgi.application'

MEDIA_ROOT = os.path.join(examcentralapppath, 'media')
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quizbuzzmaindb',
        'USER': 'quizbuzzdbadmin',
        'PASSWORD': 'qbdbadminpass',
        'HOST': 'qbmysqldbinstance.ctlpwe1tv7ia.ap-south-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'examcentraldb',
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "assets")

LOGIN_REDIRECT_URL = '/myaccount'
LOGIN_URL = '/login/'

AUTHENTICATION_BACKENDS = [
    'examcentralapp.backends.EmailOrUsernameModelBackend',    # Login w/ email
    'django.contrib.auth.backends.ModelBackend',    # Login w/ username
]

#SOCIALACCOUNT_QUERY_EMAIL = True

DEFAULT_FROM_EMAIL="support@quizbuzz.in"
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.zoho.com'

EMAIL_HOST_USER = 'support@quizbuzz.in'

EMAIL_HOST_PASSWORD = 'welcome1'

EMAIL_PORT = 587
