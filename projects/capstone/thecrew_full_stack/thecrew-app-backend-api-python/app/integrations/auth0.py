from urllib.parse import urlencode, urlunsplit
from flask import current_app, url_for


def build_authorize_url():
    return urlunsplit(
        (
            'https', current_app.config['AUTH0_DOMAIN'], '/authorize',
            _build_authorize_params(), ''))


def _build_authorize_params():
    return urlencode(
        {
            'audience': current_app.config['AUTH0_API_AUDIENCE'],
            'response_type': 'token',
            'client_id': current_app.config['AUTH0_CLIENT_ID'],
            'redirect_uri': url_for('main.welcome_callback', _external=True)
        },
        safe=':/')
