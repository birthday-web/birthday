"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

DJ_PROJECT_DIR = os.path.realpath(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)

if 'OPENSHIFT_REPO_DIR' in os.environ:
	DEPLOY=True
else:
	DEPLOY=False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!iudke*hi8vo#qyntq5yxm+p2itkuqg-m@bo8o%+cbnq(h%@@-'

# SECURITY WARNING: don't run with debug turned on in production!
if DEPLOY:
	DEBUG = False
else:
	DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
	ALLOWED_HOSTS = []
else:
	ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nocaptcha_recaptcha',
    'home',
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

# GETTING-STARTED: change 'myproject' to your project name:
ROOT_URLCONF = 'birthday.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'birthday.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
if DEPLOY:
	DB_BASE_DIR=os.environ['OPENSHIFT_DATA_DIR']
else:
	DB_BASE_DIR=BASE_DIR


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_BASE_DIR, 'db.sqlite3'),
    }
}
print '-----',(DATABASES['default'])['NAME'],'-----'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'..','..','static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

if DEPLOY:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR',''),'images')
    MEDIA_URL= '/media/'
else:
	MEDIA_ROOT = '/home/zeeshan/Desktop/Websites/openshift/birthday/wsgi/birthday/media/'
	MEDIA_URL= '/home/zeeshan/Desktop/Websites/openshift/birthday/wsgi/birthday/media/'

NORECAPTCHA_SITE_KEY = '6Ld_lQkTAAAAAIitG4r-YKH_0I_w5W-Q_WG8KzZV'
NORECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']
