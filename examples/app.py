"""A test app for pyramid-googleauth."""
from os import environ
from typing import List, NamedTuple

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.security import Allowed, Denied
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config

from pyramid_googleauth import GoogleSecurityPolicy


# Your app needs to have a Pyramid security policy that subclasses
# pyramid-googleauth's GoogleSecurityPolicy and implements the identity() and
# permits() methods.
# See https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html
class TestGoogleSecurityPolicy(GoogleSecurityPolicy):
    class Identity(NamedTuple):
        permissions: List[str]

    def identity(self, request):
        userid = self.authenticated_userid(request)

        # For this test app we're just going to give a "google" permission to
        # any user authenticated via Google. This can then be used to protect a
        # view by doing:
        #
        #   @view_config(..., permission="google")
        #
        # If your Google Cloud Platform's OAuth consent screen "User type"
        # setting is set to "External" then this will allow *any* Google user
        # to authenticate with *any* Google account and get the "google"
        # permission!
        #
        # userid will be set to the Google email address that the user has
        # authenticated with so you could assign different permissions based on
        # that. For example:
        #
        #   if userid and userid.endswith("@hypothes.is"):
        #       return self.Identity(permissions=[...])
        if userid:
            return self.Identity(permissions=["google"])

        return self.Identity([])

    def permits(self, request, _context, permission):
        if permission in self.identity(request).permissions:
            return Allowed("allowed")

        return Denied("denied")


@view_config(route_name="protected", request_method="GET", permission="google")
def protected(request):
    return Response(
        "<p>You have to be logged in to see this page.</p>"
        f"<p>Your authenticated_userid is: <code>{request.authenticated_userid}</code>.</p>"
        f"<p>Your permissions are: <code>{request.identity.permissions}</code>.</p>"
        f'<p><a href="{ request.route_url("pyramid_googleauth.logout") }">Log out</a></p>'
    )


@view_config(route_name="index", request_method="GET")
def index(request):
    return Response(
        f"<p>Your authenticated_userid is: <code>{request.authenticated_userid}</code>.</p>"
        f"<p>Your permissions are: <code>{request.identity.permissions}</code>.</p>"
        "<p>You have to be logged in to see "
        f'<a href="{ request.route_url("protected") }">the protected page</a>.</p>'
        f'<p><a href="{ request.route_url("pyramid_googleauth.login") }">Log in</a></p>'
        f'<p><a href="{ request.route_url("pyramid_googleauth.logout") }">Log out</a></p>'
    )


def app():
    config = Configurator()

    # Your app needs to have a session factory.
    # See https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/sessions.html
    config.set_session_factory(SignedCookieSessionFactory(environ["SESSION_SECRET"]))

    # Your app needs to set your security policy.
    config.set_security_policy(TestGoogleSecurityPolicy())

    settings = config.registry.settings

    # Your app needs to set the pyramid_googleauth.google_client_id and
    # pyramid_googleauth.google_client_secret settings.
    #
    # For this test app we're going to read the values for the settings from
    # environment variables, so you need to set the
    # PYRAMID_GOOGLEAUTH_CLIENT_ID and PYRAMID_GOOGLEAUTH_CLIENT_SECRET envvars
    # before running `make dev`.
    # See README.md for how to get or create the values for these envvars.
    settings["pyramid_googleauth.google_client_id"] = environ[
        "PYRAMID_GOOGLEAUTH_CLIENT_ID"
    ]
    settings["pyramid_googleauth.google_client_secret"] = environ[
        "PYRAMID_GOOGLEAUTH_CLIENT_SECRET"
    ]

    # pyramid-googleauth also needs a signing secret that it uses to generate
    # OAuth 2.0 `state` parameters to prevent cross-site scripting attacks.
    settings["pyramid_googleauth.secret"] = environ["PYRAMID_GOOGLEAUTH_SECRET"]

    # Your apps has to tell pyramid-googleauth where to direct users to after a
    # successful login.
    config.add_route("protected", "/protected")
    settings["pyramid_googleauth.login_success_redirect_url"] = "/protected"

    # Finally, activate the pyramid-googleauth extension.
    config.include("pyramid_googleauth")

    config.add_route("index", "/")
    config.scan()
    return config.make_wsgi_app()
