# Hoptcha Client for Django

Hoptcha is a modern CAPTCHA provider designed for seamless integration into web applications.
This package, `django-hoptcha`, allows Django developers to quickly integrate Hoptcha CAPTCHA validation into their views with minimal effort.

---

## 📚 Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Quick Start](#quick-start)

  * [1. Configure settings](#1-configure-settings)
  * [2. Protect a view with CAPTCHA](#2-protect-a-view-with-captcha)
  * [3. Use JavaScript integration](#3-use-javascript-integration)
* [Advanced Usage](#advanced-usage)

  * [Custom Rate-Limiting Logic](#custom-rate-limiting-logic)
  * [Combining with Django-Ratelimit](#combining-with-django-ratelimit)
  * [Custom CAPTCHA UI Rendering](#custom-captcha-ui-rendering)
  * [Custom fetch function](#custom-fetch-function)
* [Customization](#customization)
* [License](#license)

---

## ✅ Features

* 🔒 Server-side CAPTCHA verification with client and secret keys
* 🧠 Rate-limiting and conditional CAPTCHA fallback
* 🤩 Easy integration via decorators
* ⚙️ Customizable request identification (e.g., IP + user ID)
* 🧰 Built-in support for Django views and REST APIs
* 🛆 Lightweight and production-ready
* 🎨 Custom iframe rendering with `{% captcha_iframe %}`

---

## 🛠️ Installation

```bash
pip install django-hoptcha
```

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'django_hoptcha',
]
```

Collect static files:

```bash
python manage.py collectstatic
```

---

## 🚀 Quick Start

### 1. Configure settings

Add the following to your `settings.py`:

```python
HOPTCHA_URL = 'https://your-hoptcha-domain.com/captcha/validate/'
HOPTCHA_VERIFY_URL = 'https://your-hoptcha-domain.com/captcha/'
HOPTCHA_CLIENT_ID = 'your-client-key'
HOPTCHA_CLIENT_SECRET = 'your-secret-key'
```

> These credentials are provided by the Hoptcha service when you register your application.

---

### 2. Protect a view with CAPTCHA

Import the decorator and apply it to any Django view:

```python
from django_hoptcha.decorators import hoptcha_protected

@hoptcha_protected()
def my_view(request):
    return JsonResponse({'success': True})
```

This will:

* Track repeated requests using the IP address.
* Require CAPTCHA after 5 attempts (default).
* Verify the token via the configured Hoptcha endpoint.

---

### 3. Use JavaScript integration

In your template:

```html
{% load static hoptcha_tags %}
{% captcha_placeholder %}
<script src="{% static 'django_hoptcha/hoptcha.js' %}"></script>
```

Or if you want to place captcha placeholder dynamically use `<div id="hoptcha-container"></div>`.
Alternatively you can use `{% captcha_iframe %}` if your captcha is static.


In your frontend JS:

```javascript
function startPasswordReset() {
    const payload = {
        studentId: String(studentId),
        captcha_token: 'initial'
    };

    hoptchaPost('/users/send-reset/', payload, function() {
        renderResetOTPEntry();
    }, function(error) {
        showError(error);
    });
}
```

You may optionally pass a custom onCaptcha renderer if you want to override the default iframe design:

```javascript
hoptchaPost('/users/send-reset/', payload, onSuccess, onError, function customCaptchaRenderer(url) {
    // Your custom UI logic here
    showCustomModal();
    renderMyCustomCaptchaIframe(url);
});
```

---

## ⚙️ Advanced Usage

### Custom Rate-Limiting Logic

You can customize how repeated attempts are tracked using a key function:

```python
def ip_and_student_id(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    student_id = request.POST.get("studentId", "")
    return f"{ip}:{student_id}"
```

Apply it like this:

```python
@hoptcha_protected(threshold=5, timeout=300, key=ip_and_student_id)
def send_reset_code(request):
    ...
```

---

### Combining with Django-Ratelimit

This package works seamlessly with [`django-ratelimit`](https://pypi.org/project/django-ratelimit/):

```python
from ratelimit.decorators import ratelimit
from django_hoptcha.decorators import hoptcha_protected

@ratelimit(key='ip', rate='15/m', method='POST', block=True)
@hoptcha_protected(threshold=5, timeout=300)
def secure_view(request):
    ...
```

The `@ratelimit` decorator enforces strict rate limits while `@hoptcha_protected` provides a soft CAPTCHA fallback.

### Custom CAPTCHA UI Rendering

You can override the default iframe and style using the optional onCaptcha parameter in the hoptchaPost() JavaScript function. This is useful if you want to match your app’s branding or use modals.

```javascript
hoptchaPost('/endpoint', payload, onSuccess, onError, function renderCustom(url) {
    // Replace container with your custom implementation
    document.getElementById('myCustomCaptchaArea').innerHTML = `<iframe src="${url}"></iframe>`;
});
```

### Custom fetch function

You can use custom fetch function to handle requests. This can be useful in cases where you want to pass custom headers like CSRF protection headers.

```javascript
configureHoptcha({
    fetcher: fetchWithAuth
});
```

---

## 🔧 Customization

| Parameter      | Description                                                  | Default       |
|----------------|--------------------------------------------------------------|---------------|
| `key`          | Function or string to identify requestor (IP, user ID, etc.) | `ip`          |
| `threshold`    | Number of allowed attempts before CAPTCHA is required        | `5`           |
| `timeout`      | Time in seconds to reset attempt count                       | `300` (5 min) |
| `backoff`      | Exponentially increase timeout if repeatedly exceeded        | `False`       |
| `response`     | Optional custom response function on CAPTCHA failure         | `None`        |
| `exempt_if`    | Skip protection for trusted users                            | For staff     |
| `methods`      | HTTP methods to track (POST, GET, etc.)                      | POST          |
| `shared`       | Share same attempts counter among all endpoints              | `False`       |
| `type`         | Type of CAPTCHA do display (sliding, pointing, random)       | `random`      |
| `debug_ignore` | Do not bypass CAPTCHA if in debug mode                       | `False`       |

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Open issues or pull requests on [Git](https://git.hopsenn.com/hopsenn/django-hoptcha).
