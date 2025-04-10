from django.conf import settings


def settings_context(request):
    return {
        "DEBUG": settings.DEBUG,
        "BASE_DIR": settings.BASE_DIR,
        "SECRET_KEY": settings.SECRET_KEY,
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
        "INSTALLED_APPS": settings.INSTALLED_APPS,
        "MIDDLEWARE": settings.MIDDLEWARE,
        "ROOT_URLCONF": settings.ROOT_URLCONF,
        "TEMPLATES": settings.TEMPLATES,
        "WSGI_APPLICATION": settings.WSGI_APPLICATION,
        "DATABASES": settings.DATABASES,
        "AUTH_PASSWORD_VALIDATORS": settings.AUTH_PASSWORD_VALIDATORS,
        "LANGUAGE_CODE": settings.LANGUAGE_CODE,
        "TIME_ZONE": settings.TIME_ZONE,
        "USE_I18N": settings.USE_I18N,
        "USE_TZ": settings.USE_TZ,
        "STATIC_URL": settings.STATIC_URL,
        "STATICFILES_DIRS": settings.STATICFILES_DIRS,
        "DEFAULT_AUTO_FIELD": settings.DEFAULT_AUTO_FIELD,
        "REST_FRAMEWORK": settings.REST_FRAMEWORK,
    }
