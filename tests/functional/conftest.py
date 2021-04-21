import pyramid
import pytest
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from webtest import TestApp

from pyramid_googleauth._routes import add_routes
from tests.functional.mock_services import (  # pylint:disable=unused-import
    mock_google_auth_service,
)
from tests.functional.services import signature_service  # pylint:disable=unused-import


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
def logged_in(
    app, route_url, signature_service, mock_google_auth_service
):  # pylint: disable=unused-argument
    """Make `app` be logged in to the admin pages with a session cookie."""
    # Google redirects the browser to our login callback URL with a state
    # param, and the login callback URL's response includes a session cookie in
    # a Set-Cookie header to log the browser in. Simulate that redirect
    # response so that the logged-in session cookie gets stored in
    # `app.cookiejar`. Webtest will automatically send the cookie in subsequent
    # requests made with `app`.
    app.get(
        route_url("pyramid_googleauth_login_callback"),
        params={"state": signature_service.get_nonce()},
    )


@pytest.fixture
def pyramid_app(pyramid_settings, policy):

    config = pyramid.config.Configurator(settings=pyramid_settings)
    config.include("pyramid_services")
    config.include("pyramid_googleauth")
    add_routes(config)

    session_factory = SignedCookieSessionFactory(
        pyramid_settings["pyramid_googleauth.secret"],
        serializer=pyramid.session.JSONSerializer(),
    )
    config.set_session_factory(session_factory)
    config.set_security_policy(policy)

    def protected_view(_context, _request):
        return Response(body="ok", status=200)

    def logged_out(request):
        return HTTPFound(location=request.route_url("pyramid_googleauth_login"))

    config.add_view(protected_view, route_name="protected_view", permission="admin")
    config.add_route("protected_view", "/inside")
    config.add_forbidden_view(logged_out)

    return config.make_wsgi_app()
