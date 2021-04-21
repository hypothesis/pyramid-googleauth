from unittest import mock

import pytest
from pyramid import testing
from pyramid.request import apply_request_extensions
from pyramid.testing import DummyRequest

from pyramid_googleauth._routes import add_routes
from pyramid_googleauth.services import SignatureService
from tests.unit.services import *  # pylint: disable=wildcard-import,unused-wildcard-import


@pytest.fixture
def pyramid_config(pyramid_settings):
    with testing.testConfig(settings=pyramid_settings) as config:
        add_routes(config)

        yield config


@pytest.fixture
def pyramid_request(
    pyramid_config,  # pylint:disable=unused-argument
):
    pyramid_request = DummyRequest(environ={"HTTP_HOST": "example.com"})
    apply_request_extensions(pyramid_request)
    return pyramid_request


@pytest.fixture
def signature_service():
    return mock.create_autospec(SignatureService, spec_set=True, instance=True)
