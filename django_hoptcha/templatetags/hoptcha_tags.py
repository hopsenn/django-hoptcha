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

from django import template
from django_hoptcha.settings import (
    HOPTCHA_URL,
    HOPTCHA_CLIENT_ID,
)

from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def captcha_placeholder():
    return render_to_string('django_hoptcha/captcha_placeholder.html', {})


@register.simple_tag
def captcha_iframe():
    context = {
        'captcha_url': HOPTCHA_URL,
        'public_key': HOPTCHA_CLIENT_ID,
    }
    return render_to_string('django_hoptcha/captcha_iframe.html', context)
