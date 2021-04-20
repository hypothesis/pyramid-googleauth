import functools
from unittest import mock

import pytest

from pyramid.testing import DummyRequest, testConfig

from h_pyramid_google_oauth.routes import add_routes


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
        "h_pyramid_google_oauth.secret": "not-very-secret",
        "h_pyramid_google_oauth.google_client_id": "google_client_id",
        "h_pyramid_google_oauth.google_client_secret": "google_client_secret",
        "h_pyramid_google_oauth.login_success_redirect_url": "http://example.com/inside",
    }


@pytest.fixture
def route_url():
    request = DummyRequest(environ={"SERVER_NAME": "localhost"})

    with testConfig(request=request) as config:
        add_routes(config)
        yield functools.partial(request.route_url, _scheme="https")
