from unittest.mock import sentinel

import pytest
from webtest import TestApp

from examples.app import app as demo_app


@pytest.fixture
def app(pyramid_app):
    # This extra_environ is necessary to get webtest to use https and port
    # 443 when you give it a path rather than a full URL `app.get("/foo/bar")`.
    # We need it to use SSL because the admin pages use secure cookies
    return TestApp(
        pyramid_app,
        extra_environ={"wsgi.url_scheme": "https", "HTTP_HOST": "localhost:443"},
    )


@pytest.fixture
def logged_in(app, route_url, mock_google_auth_service):
    """Make `app` be logged in to the admin pages with a session cookie."""
    # Google redirects the browser to our login callback URL with a state
    # param, and the login callback URL's response includes a session cookie in
    # a Set-Cookie header to log the browser in. Simulate that redirect
    # response so that the logged-in session cookie gets stored in
    # `app.cookiejar`. Webtest will automatically send the cookie in subsequent
    # requests made with `app`.
    app.get(
        route_url("pyramid_googleauth.login.callback"),
        params={  # pylint: disable=protected-access
            "state": mock_google_auth_service._get_nonce()
        },
    )


@pytest.fixture
def environment(monkeypatch, pyramid_settings):
    monkeypatch.setenv(
        "PYRAMID_GOOGLEAUTH_CLIENT_ID",
        pyramid_settings["pyramid_googleauth.google_client_id"],
    )
    monkeypatch.setenv(
        "PYRAMID_GOOGLEAUTH_CLIENT_SECRET",
        pyramid_settings["pyramid_googleauth.google_client_secret"],
    )
    monkeypatch.setenv(
        "PYRAMID_GOOGLEAUTH_SECRET", pyramid_settings["pyramid_googleauth.secret"]
    )
    monkeypatch.setenv(
        "GOOGLEAUTH_SUCCESS_REDIRECT_URL",
        pyramid_settings["pyramid_googleauth.login_success_redirect_url"],
    )

    monkeypatch.setenv("SESSION_SECRET", pyramid_settings["pyramid_googleauth.secret"])


@pytest.fixture
def pyramid_app(environment):  # pylint: disable=unused-argument
    return demo_app()


@pytest.fixture
def mock_google_auth_service(patch):
    MockGoogleAuthService = patch(
        "pyramid_googleauth.services.google_auth.GoogleAuthService"
    )
    mock_google_auth_service = MockGoogleAuthService.return_value
    mock_google_auth_service.exchange_auth_code.return_value = (
        {"email": "user@hypothes.is"},
        sentinel.credentials,
        {},
    )
    return mock_google_auth_service
