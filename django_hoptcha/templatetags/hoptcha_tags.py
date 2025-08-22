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
