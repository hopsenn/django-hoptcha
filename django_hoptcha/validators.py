import json
import requests

from .settings import (
    HOPTCHA_VERIFY_URL,
    HOPTCHA_CLIENT_ID,
    HOPTCHA_CLIENT_SECRET
)


def verify_token(token):
    try:
        payload = {
            "token": token,
            "client_key": HOPTCHA_CLIENT_ID,
            "client_secret": HOPTCHA_CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(HOPTCHA_VERIFY_URL, data=json.dumps(payload), headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json().get("success", False)
        return False

    except Exception:
        return False
