# Django settings for code_project project.
import sys, os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def rel_to(to, *x):
    return os.path.join(to, *x)

sys.path.append(PROJECT_ROOT)
sys.path.append(rel("apps"))

#DISTR_DIR='/home/german/distr'
#LIB_DIR='/home/german/work/libs'

DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'atboard', # Or path to database file if using sqlite3.
        'USER': 'atboard', # Not used with sqlite3.
        'PASSWORD': 'atboard', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Almaty'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ("ru", "Russian"),
    ("en", "English"),
#    ("kz","Kazakh"),
#    ("tr","Turkish"),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

DATE_INPUT_FORMATS = (
    '%d.%m.%Y', # '25.10.2006'
#    '%d/%m/%Y', '%d/%m/%y',     # '25/10/2006', '25/10/06'
#    '%Y-%m-%d', '%y-%m-%d',     # '2006-10-25', '06-10-25'
)

#DATETIME_INPUT_FORMATS = (
#    '%d/%m/%Y %H:%M:%S',    # '25/10/2006 14:30:59'
#    '%d/%m/%Y %H:%M',       # '25/10/2006 14:30'
#    '%d/%m/%y %H:%M:%S',    # '25/10/06 14:30:59'
#    '%d/%m/%y %H:%M',       # '25/10/06 14:30'
#    '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
#    '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
#    '%Y-%m-%d',             # '2006-10-25'
#    '%d.%m.%Y %H:%M',
#)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('../../media/atboard/')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x7+2eb0f2zd_to48j11jrrk*j*bm_4k$%w%(%h0_1f-33mdrd*'

#email stuff
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'atboard.kz@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[atboard.kz] '
SERVER_EMAIL = 'no-reply@atboard.kz'
DEFAULT_FROM_EMAIL = 'no-reply@atboard.kz'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.app_directories.load_template_source'
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'sso.middleware.SingleSignOnMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.UserLanguageMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'atboard.urls'

TEMPLATE_DIRS = (
    rel('templates'),
)

#ROBOTS_SITEMAP_URLS = ['http://www.buben.kz/sitemap.xml']


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.sitemaps',

#    'django-backup',
#    'tagging',
    'south',
#    'sorl.thumbnail',
#    'basic.inlines',
#    'photologue',
#    'haystack',
    'robots',
    'uni_form',
    'registration',
#    'invitation',

    'eplace',
    'common',
    'etcs',
#    'sso',
)

DEANS_GROUP = 'Deans'
TEACHERS_GROUP = 'Teachers'
SUPERVISERS_GROUP = 'Supervisers'
ABSENCE_PERCENTAGE_LIMIT = 20
TICK_VALUES = (
    (-2, 'L', 'Late'),
    (-1, 'I', 'Ill'),
    (0, '-', 'Absent'),
    (1, '+', 'Attended'),
)
ABSENCE_VALUES = (-1, 0,)

try:
    from local_settings import *
except ImportError:
    pass

THUMBNAIL_EXTENSION = 'png'
THUMBNAIL_DEBUG = DEBUG

#invitation
INVITE_MODE = True
ACCOUNT_INVITATION_DAYS = 15
INVITATIONS_PER_USER = 50

# we need this for registration stuff
REQUIRE_EMAIL_CONFIRMATION = True
ACCOUNT_ACTIVATION_DAYS = ACCOUNT_INVITATION_DAYS
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'eplace':{
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
