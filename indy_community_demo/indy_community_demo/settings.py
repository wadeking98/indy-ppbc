import os
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o!@$s09c&n$y+=(sc)i14ogy=t!p_%y%mczu-@6kh2%zoe14y*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'indy_community.apps.IndyCoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'background_task',
    'imms_demo',
    'indy_community_demo',
]

def file_ext():
    if platform.system() == 'Linux':
        return '.so'
    elif platform.system() == 'Darwin':
        return '.dylib'
    elif platform.system() == 'Windows':
        return '.dll'
    else:
        return '.so'

INDY_CONFIG = {
    'storage_dll': 'libindystrgpostgres' + file_ext(),
    'storage_entrypoint': 'postgresstorage_init',
    'payment_dll': 'libnullpay' + file_ext(),
    'payment_entrypoint': 'nullpay_init',
    'wallet_config': {'id': '', 'storage_type': 'postgres_storage'},
    'wallet_credentials': {'key': ''},
    'storage_config': {'url': 'localhost:5432'},
    'storage_credentials': {'account': 'postgres', 'password': 'mysecretpassword', 'admin_account': 'postgres', 'admin_password': 'mysecretpassword'},
    'vcx_agency_url': 'http://localhost:8080',
    'vcx_agency_did': 'VsKV7grR1BUE29mG2Fm2kX',
    'vcx_agency_verkey': 'Hezce2UWMZ3wUhVkh2LfKSs8nDzWwzs2Win7EzNN3YaR',
    'vcx_payment_method': 'null',
    'vcx_enterprise_seed': '000000000000000000000000Trustee1',
    'vcx_institution_seed': '00000000000000000000000000000000',
    'vcx_genesis_path': '/tmp/atria-genesis.txt',
    'register_dids': True,
    'ledger_url': 'http://localhost:9000',
}

INDY_PROFILE_VIEW = 'imms_demo.views.profile_view'
INDY_ORG_DATA_VIEW = 'imms_demo.views.data_view'
INDY_WALLET_VIEW = 'imms_demo.views.wallet_view'

BACKGROUND_TASK_RUN_ASYNC = False
BACKGROUND_TASK_ASYNC_THREADS = 1
MAX_ATTEMPTS = 1

AUTH_USER_MODEL = 'indy_community.IndyUser'
INDY_ORGANIZATION_MODEL = 'indy_community.IndyOrganization'
INDY_ORG_RELATION_MODEL = 'indy_community.IndyOrgRelationship'

INDY_CONVERSATION_CALLBACK = 'imms_demo.views.conversation_callback'

FIXTURE_DIRS = (
   'indy_community_demo/fixtures/',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'indy_community_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'imms_demo/templates'),
        ],
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

WSGI_APPLICATION = 'indy_community_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
