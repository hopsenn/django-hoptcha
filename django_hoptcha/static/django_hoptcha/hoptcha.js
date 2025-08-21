// ==================== HOPTCHA CLIENT (Vanilla JS) ====================

(function (window) {
    /**
     * Handle messages from the iframe.
     */
    window.addEventListener("message", function (event) {
        const { token } = event.data || {};

        if (token && typeof window._captchaSuccessCallback === 'function') {
            const callback = window._captchaSuccessCallback;
            window._captchaSuccessCallback = null;  // clear after use
            callback(token);  // Send token to original requester
        }
    });

    /**
     * Renders the Hoptcha iframe inside #hoptcha-container.
     * @param {string} url - The Hoptcha URL endpoint.
     */
    window.renderCaptchaStep = function (url) {
        const container = document.getElementById("hoptcha-container");
        if (container) {
            container.innerHTML = `
                <iframe
                    id="captcha-iframe"
                    src="${url}"
                    style="width: 100%; height: 250px; border: none; border-radius: 12px;"
                ></iframe>
            `;
        }
    };

    window.configureHoptcha = function ({ fetcher }) {
        if (fetcher) window.hoptchaFetcher = fetcher;
    };

    /**
     * Utility for retrying failed requests that require CAPTCHA.
     * @param {string} url - The POST endpoint.
     * @param {object} payload - Payload to send, must include `captcha_token`.
     * @param {function} onSuccess - Success handler.
     * @param {function} [onError] - Error fallback.
     * @param {function} [onCaptcha] - Optional custom render callback.
     */
    window.hoptchaPost = function (url,
                                   payload,
                                   onSuccess, onError, onCaptcha) {
        const fetcher = window.hoptchaFetcher || fetch;

        fetcher(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            return response.json().then(data => {
                return { ok: response.ok, data };
            });
        })
        .then(({ ok, data }) => {
            const captchaNeeded = data?.captcha === true;
            const captchaUrl = data?.url;

            if (captchaNeeded && captchaUrl) {
                // Register retry callback
                window._captchaSuccessCallback = function (token) {
                    payload.captcha_token = token;
                    window.hoptchaPost(url, payload, onSuccess, onError, onCaptcha);
                };

                const render = onCaptcha || window.renderCaptchaStep;
                render(captchaUrl);
                return;
            }

            if (ok) {
                if (onSuccess) onSuccess(data);
            } else {
                const error = data?.error || 'Something went wrong.';
                if (onError) onError(error);
                else console.error(error);
            }
        })
        .catch(err => {
            const fallback = typeof err === 'string' ? err : err?.data?.error || 'Something went wrong.';
            if (onError) onError(fallback);
            else console.error(fallback);
        });
    };
})(window);
