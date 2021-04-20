# pylint: disable=too-many-ancestors

from pyramid.httpexceptions import HTTPServerError, HTTPUnauthorized


class BadOAuth2Config(HTTPServerError):
    """Something is wrong with the OAuth2 configuration of our app."""


class UserNotAuthenticated(HTTPUnauthorized):
    """A user has failed authentication."""

    # This is not the same as a service to service authentication failure
