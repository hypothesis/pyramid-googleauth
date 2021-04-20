from pyramid import testing
from pyramid.request import apply_request_extensions
from pyramid.testing import DummyRequest

from h_pyramid_google_oauth.routes import add_routes
from tests.unit.services import *  # pylint: disable=wildcard-import,unused-wildcard-import


@pytest.fixture
def pyramid_config(pyramid_settings):
    with testing.testConfig(settings=pyramid_settings) as config:
        config.include("pyramid_services")

        add_routes(config)

        yield config


@pytest.fixture
def pyramid_request(
    pyramid_config,  # pylint:disable=unused-argument
):
    pyramid_request = DummyRequest(environ={"HTTP_HOST": "example.com"})
    apply_request_extensions(pyramid_request)
    return pyramid_request
