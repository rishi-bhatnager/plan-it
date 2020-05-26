"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BASE_URL = pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(b#ey14m2um2gyu#vcv_tu_befsizv*gveu_s6sey8j6@d8v5i'


#checks if app is running locally:
import socket
HOST = socket.gethostname()
local = ".local" in HOST or "A1JHHVQ" in HOST
# print(local)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local                                                                                                #change later


ALLOWED_HOSTS = ['*'] if os.getenv('GAE_APPLICATION', None) else ['.pythonanywhere.com', '127.0.0.1']                                                         #not safe to use wildcard if deploying outside of GCP

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# Application definition

INSTALLED_APPS = [
    'webapp.apps.PlannerWrapperConfig',
    'webapp.apps.UsersWrapperConfig',
    # 'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',                                                                                     uncomment
    # # 'social_app',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                                                             #might need to change depending on where other files (e.g. html) are located
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

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


#Below = establishes connection to GCP SQL servers

# Install PyMySQL as mysqlclient/MySQLdb to use Django's mysqlclient adapter
# See https://docs.djangoproject.com/en/2.1/ref/databases/#mysql-db-api-drivers
# for more information
import pymysql  # noqa: 402
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/planner-app-265519:us-east1:planner',                    #replace last block (after /) with ~connection name~ of SQL server
            'USER': 'planner-user',                                                                  #replace with SQL DB user
            'PASSWORD': 'smith-gang-v3',                                                            #replace with SQL DB user password
            'NAME': 'planner',                                                                       #replace with database name
        }
    }

elif not local:
    # running remotely but not on GCP
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'sql_mode': 'STRICT_TRANS_TABLES',
            },
            'HOST': 'rishibhat.mysql.pythonanywhere-services.com',
            'PORT': '3306',
            'NAME': 'rishibhat$default',
            'USER': 'rishibhat',
            'PASSWORD': 'smithgirlscscscs',
        }
    }

else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {                                                                                #see above if statement for necessary replacements
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'sql_mode': 'traditional',
            },
            'HOST': 'localhost',
            'PORT': '3306',
            'NAME': 'planner',
            'USER': 'planner-local',
            'PASSWORD': 'smith-gang-v3',
        }
    }
# [END db_setup]



#Below = default
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}"""






# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Configuring Google login
# AUTHENTICATION_BACKENDS = (                                                                                   uncomment
#  'django.contrib.auth.backends.ModelBackend',
#  'allauth.account.auth_backends.AuthenticationBackend',
#  )
# SITE_ID = 1
# LOGIN_REDIRECT_URL = '/'
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }


# Django login settings
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'users:login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'connect2planit@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('PLANIT_APP_GMAIL_PASSWORD')
    # ^ environment variable PLANNER_APP_GMAIL_PASSWORD is for rishi's gmail
DEFAULT_FROM_EMAIL = 'connect2planit@gmail.com'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# LOGOUT_REDIRECT_URL = '/users/logout'
    # ^ caused some problems, prob leave commented out


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, '../collect_static')
STATIC_URL = '/static/'
