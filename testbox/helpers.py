
from django.conf import settings
from django.contrib.auth import login
from django.test.client import RequestFactory
from django.utils.importlib import import_module


def client_login(client, user):
    request = RequestFactory().request()
    request.LANGUAGE_CODE = 'en'
    request.user = user
    request.user.backend = "django.contrib.auth.backends.ModelBackend"
    request.session = {}

    engine = import_module(settings.SESSION_ENGINE)
    session_cookie = settings.SESSION_COOKIE_NAME
    session = engine.SessionStore()
    request.session = session
    request.cookie_demand = []
    login(request, user)
    request.session.save()
    client.cookies[session_cookie] = session.session_key
    cookie_data = {
        'max-age': None,
        'path': '/',
        'domain': settings.SESSION_COOKIE_DOMAIN,
        'secure': settings.SESSION_COOKIE_SECURE or None,
        'expires': None,
    }
    client.cookies[session_cookie].update(cookie_data)
    return user
