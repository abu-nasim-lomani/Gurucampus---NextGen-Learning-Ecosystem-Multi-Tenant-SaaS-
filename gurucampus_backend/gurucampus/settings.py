from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$4-5ali@^$8q$a*zf2e2m-gps-8ye@t@n++hr@0f%qa$ro@+sw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "admin.localhost",
    "brac.localhost",
    # ভবিষ্যতে আমরা এখানে brac.localhost, aci.localhost ইত্যাদি যোগ করবো
]

# As per Architecture Guide (B.1)
SHARED_APPS = [
    "django_tenants",  # Must be first
    "tenants",         # Our custom tenant management app
    "subscriptions",   # Manages B2B Tenant Plans
    
    # --- 'courses', 'assessments', 'marketplace' এখান থেকে সরানো হয়েছে ---

    # Django core apps
    "django.contrib.contenttypes", 
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

TENANT_APPS = [
    # Django core apps for tenants
    "django.contrib.admin",
    "django.contrib.auth",

    # 3rd-party apps
    "rest_framework",
    "rest_framework_simplejwt",

    # --- এটিই চূড়ান্ত এবং সঠিক "ওয়ার্ল্ড-ক্লাস" আর্কিটেকচার ---
    "users",         # Tenant-specific users
    "academics",     # Tenant-specific classes
    "courses",       # Tenant-specific courses (ফিরে এসেছে)
    "assessments",   # Tenant-specific assessments (ফিরে এসেছে)
    "marketplace",   # Tenant-specific B2C logic (ফিরে এসেছে)
]
# Application definition

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]


TENANT_MODEL = "tenants.Organization"
TENANT_DOMAIN_MODEL = "tenants.Domain"


MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'gurucampus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gurucampus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)


DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",  # <-- এটি পরিবর্তন করুন
        "NAME": "gurucampus_db",                      # আপনার ডাটাবেসের নাম
        "USER": "postgres",                           # আপনার PostgreSQL ইউজার
        "PASSWORD": "Bx@123$321",                  # আপনার পাসওয়ার্ড
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "users.CustomUser"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


# --- Celery (Redis) Configuration ---
# This tells Celery where the "order rail" (Redis) is.
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'




JUDGE0_API_URL = "https://judge0-ce.p.rapidapi.com"
JUDGE0_API_KEY = "7e8db262dfmsh378de1895b4ea53p1caa9bjsn0a74c16a02fe"


# URL je-ta browser file-guloke khujte bebohar korbe.
# Udahoron: http://brac.localhost:8000/media/lessons/files/slide.pdf
MEDIA_URL = "/media/"

# Server-er file system-e file-gulo kothay save hobe tar shothik poth.
# (amader `gurucampus_backend` folder-er vitore 'media' name ekta folder toiri korbe)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")