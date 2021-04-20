from unittest import mock

import pytest

from pyramid_googleauth.services import GoogleAuthService, SignatureService


@pytest.fixture
def mock_service(pyramid_config):
    def mock_service(service_class):
        mock_service = mock.create_autospec(service_class, spec_set=True, instance=True)
        pyramid_config.register_service(mock_service, iface=service_class)

        return mock_service

    return mock_service


@pytest.fixture
def signature_service(mock_service):
    signature_service = mock_service(SignatureService)
    signature_service.sign_items.return_value = "secure_token"
    return signature_service


@pytest.fixture
def google_auth_service(mock_service):
    return mock_service(GoogleAuthService)
