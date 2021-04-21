import functools
from unittest import mock

import pytest
from pyramid.security import Allowed, Denied
from pyramid.testing import DummyRequest, testConfig

from pyramid_googleauth._routes import add_routes
from pyramid_googleauth.security import GoogleSecurityPolicy


def _autopatcher(request, target, **kwargs):
    """Patch and cleanup automatically. Wraps :py:func:`mock.patch`."""
    options = {"autospec": True}
    options.update(kwargs)
    patcher = mock.patch(target, **options)
    obj = patcher.start()
    request.addfinalizer(patcher.stop)
    return obj


@pytest.fixture
def patch(request):
    return functools.partial(_autopatcher, request)


@pytest.fixture
def pyramid_settings():
    return {
        "pyramid_googleauth.secret": "not-very-secret",
        "pyramid_googleauth.google_client_id": "google_client_id",
        "pyramid_googleauth.google_client_secret": "google_client_secret",
        "pyramid_googleauth.login_success_redirect_url": "http://example.com/inside",
    }


@pytest.fixture
def route_url():
    request = DummyRequest(environ={"SERVER_NAME": "localhost"})

    with testConfig(request=request) as config:
        add_routes(config)
        yield functools.partial(request.route_url, _scheme="https")


class DummyGoogleSecurityPolicy(GoogleSecurityPolicy):
    def identity(self, request):
        userid = self.authenticated_userid(request)

        if userid and userid.endswith("@hypothes.is"):
            return ["admin"]

        return []

    def permits(self, request, context, permission):
        if permission in self.identity(request):
            return Allowed("allowed")

        return Denied("denied")


@pytest.fixture
def policy():
    return DummyGoogleSecurityPolicy()
