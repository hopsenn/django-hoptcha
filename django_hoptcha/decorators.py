"""
MIT License

Copyright (c) 2025 Hopsenn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import json

from urllib.parse import urlencode

from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse

from .validators import verify_token
from .settings import (
    HOPTCHA_URL,
    HOPTCHA_CLIENT_ID,
    DEBUG
)

# Built-in key functions
def get_ip(group, request):
    return request.META.get('REMOTE_ADDR', 'unknown-ip')

def user_or_session(group, request):
    if request.user.is_authenticated:
        return str(request.user.pk)
    return request.session.session_key or request.META.get("REMOTE_ADDR")

def get_user(group, request):
    return str(request.user.id) if request.user.is_authenticated else None

def get_user_or_ip(group, request):
    return get_user(request) or get_ip(request)

BUILTIN_KEYS = {
    'ip': get_ip,
    'user': get_user,
    'user_or_ip': get_user_or_ip,
    'user_or_session': user_or_session
}

def hoptcha_protected(
    threshold=5,
    timeout=300,
    key="ip",
    methods=["POST"],
    response=None,
    exempt_if=lambda request: request.user.is_staff or request.user.is_superuser,
    backoff=False,
    shared=False,
    type=None,
    debug_ignore=False
):
    """
    Enforces CAPTCHA if request exceeds `threshold`.

    - key: 'ip', 'user', 'user_or_ip', or custom function.
    - threshold: # of allowed unauthenticated attempts before requiring CAPTCHA.
    - timeout: seconds to keep attempt count in cache.
    - backoff: exponentially increase timeout if repeatedly exceeded.
    - response: optional custom response function on CAPTCHA failure.
    - exempt_if: skip protection for trusted users.
    - methods: HTTP methods to track (default: POST).
    - shared: Share same attempts counter among all endpoints.
    - type: Type of CAPTCHA do display (sliding, pointing, random)
    - debug_ignore: do not bypass CAPTCHA if in debug mode.
    """

    if isinstance(key, str):
        key_func = BUILTIN_KEYS.get(key)

        if not key_func:
            raise ValueError(f"Unknown key: {key}")

    elif callable(key):
        key_func = key

    else:
        raise TypeError("key must be a string or callable")

    type = type.lower() if type and type.lower() in ['sliding', 'pointing'] else 'random'

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if DEBUG and not debug_ignore:
                return view_func(request, *args, **kwargs)

            if exempt_if and exempt_if(request):
                return view_func(request, *args, **kwargs)

            if request.method not in methods:
                return view_func(request, *args, **kwargs)

            user_key = key_func(None, request)
            if not shared:
                user_key = f"{user_key}:{request.path}"

            cache_key = f"hoptcha-attempts:{user_key}"
            attempts = cache.get(cache_key, 0)

            if attempts >= threshold:
                token = (
                    request.POST.get("captcha_token") or
                    request.GET.get("captcha_token")
                )

                # Try extracting from JSON body if not found yet
                if not token and request.content_type == "application/json":
                    try:
                        body = json.loads(request.body)
                        token = body.get("captcha_token")
                    except (json.JSONDecodeError, TypeError):
                        pass  # Malformed or empty JSON

                if not token or not verify_token(token):
                    return response(request) if response else JsonResponse({
                        "captcha": True,
                        "url": f"{HOPTCHA_URL}?{urlencode({'client_key': HOPTCHA_CLIENT_ID, 'timestamp': int(time.time() * 1000), 'type': type})}"
                    }, status=200)
                else:
                    cache.delete(cache_key)  # reset counter if passed
                    return view_func(request, *args, **kwargs)

            timeout_val = timeout * (2 ** (attempts - threshold)) if backoff and attempts >= threshold else timeout
            cache.set(cache_key, attempts + 1, timeout=timeout_val)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
