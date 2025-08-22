from django.conf import settings

def get(key, default=None):
    return getattr(settings, key, default)

HOPTCHA_URL = get('HOPTCHA_URL', 'https://hoptcha.com/api/v1/captcha/')
HOPTCHA_VERIFY_URL = get('HOPTCHA_VERIFY_URL', 'https://hoptcha.com/api/v1/captcha/validate/')

HOPTCHA_CLIENT_ID = get('HOPTCHA_CLIENT_ID', '')
HOPTCHA_CLIENT_SECRET = get('HOPTCHA_CLIENT_SECRET', '')

DEBUG = get('DEBUG', False)
