from unittest.mock import sentinel

import pytest
from h_matchers import Any
from jwt import InvalidTokenError
from oauthlib.oauth2.rfc6749.errors import InvalidClientError, InvalidGrantError

from pyramid_googleauth.exceptions import BadOAuth2Config, UserNotAuthenticated
from pyramid_googleauth.services.google_auth import GoogleAuthService, factory

# We do this all the time here, but it's ok for the tests of a file to poke
# about in the innards of that file
# pylint: disable=protected-access


class TestGoogleAuthService:
    @pytest.mark.parametrize(
        "redirect_uri,insecure",
        (("http://example.com", True), ("https://example.com", False)),
    )
    def test_it_allows_non_https_redirect_uris_for_dev(
        self, redirect_uri, client_config, insecure, os
    ):
        os.environ = {}
        client_config["redirect_uri"] = redirect_uri

        GoogleAuthService(sentinel.secret, client_config=client_config)

        assert bool(os.environ.get("OAUTHLIB_INSECURE_TRANSPORT")) == insecure

    @pytest.mark.usefixtures("_get_nonce", "_decode_state", "base64")
    def test_getting_a_flow(self, service, client_config, flow, Flow):
        # We aren't interested in login_url, but it triggers the call
        service.login_url()

        Flow.from_client_config.assert_called_once_with(
            {
                "web": {
                    "client_id": client_config["client_id"],
                    "client_secret": client_config["client_secret"],
                    "auth_uri": service.OPEN_ID_DISCOVERY["authorization_endpoint"],
                    "token_uri": service.OPEN_ID_DISCOVERY["token_endpoint"],
                }
            },
            scopes=service.SCOPES,
        )

        assert flow.redirect_uri == client_config["redirect_uri"]

    def test_getting_a_flow_raises_with_bad_config(self, service, Flow):
        # The google library raises a very vague error when this happens
        Flow.from_client_config.side_effect = ValueError

        with pytest.raises(BadOAuth2Config):
            # We aren't interested in login_url, but it triggers the call
            service.login_url()

    def test_login_url_base_case(self, _check_nonce, service, flow, base64, json, jwt):
        url = service.login_url(next_="/next")

        flow.authorization_url.assert_called_once_with(
            access_type="offline",
            include_granted_scopes="true",
            login_hint=Any(),
            state=base64.urlsafe_b64encode.return_value,
            prompt=Any(),
        )

        json.dumps.assert_called_once_with(
            {"next": "/next", "nonce": jwt.encode.return_value}
        )
        authorization_url, _ = flow.authorization_url.return_value

        assert url == authorization_url
        _check_nonce.assert_called_once_with(json.loads.return_value.get.return_value)

    @pytest.mark.parametrize("login_hint", (None, "staff@hypothes.is"))
    @pytest.mark.parametrize("force_login", (True, False))
    @pytest.mark.usefixtures("base64")
    def test_login_url_variations(self, service, flow, login_hint, force_login):
        service.login_url(login_hint, force_login)

        flow.authorization_url.assert_called_once_with(
            access_type=Any(),
            include_granted_scopes=Any(),
            login_hint=login_hint,
            state=Any(),
            prompt="select_account" if force_login else None,
        )

    @pytest.mark.usefixtures("flow", "base64")
    def test_login_url_verifies_the_state(self, service, _check_nonce):
        _check_nonce.return_value = False

        with pytest.raises(UserNotAuthenticated):
            service.login_url()

    @pytest.mark.usefixtures("base64")
    def test_exchange_auth_code_works(self, service, flow, jwt, _check_nonce, json):
        redirect_url = "http://example.com?state=state_value"

        user_details, credentials, state = service.exchange_auth_code(redirect_url)

        flow.fetch_token.assert_called_once_with(authorization_response=redirect_url)
        jwt.decode.assert_called_once_with(
            flow.credentials.id_token, options=dict(verify_signature=False)
        )

        # We extract and check the state/nonce
        _check_nonce.assert_called_once_with(json.loads.return_value.get.return_value)

        assert user_details == jwt.decode.return_value
        assert credentials == {
            "token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token,
            "id_token": flow.credentials.id_token,
            "token_uri": flow.credentials.token_uri,
            "client_id": flow.credentials.client_id,
            "client_secret": flow.credentials.client_secret,
            "scopes": flow.credentials.scopes,
        }

    def test_exchange_auth_code_checks_for_returned_errors(self, service):
        with pytest.raises(UserNotAuthenticated):
            service.exchange_auth_code("http://example.com?error=oh_dear")

    def test_exchange_auth_code_checks_the_state(self, service, _check_nonce):
        _check_nonce.return_value = False
        with pytest.raises(UserNotAuthenticated):
            service.exchange_auth_code("http://example.com?state=BAD_STATE")

    def test_exchange_auth_code_raises_if_user_not_authed(self, service, flow):
        flow.fetch_token.side_effect = InvalidGrantError

        with pytest.raises(UserNotAuthenticated):
            service.exchange_auth_code("http://example.com?state=state_value")

    def test_exchange_auth_code_raises_if_oauth_values_bad(self, service, flow):
        flow.fetch_token.side_effect = InvalidClientError

        with pytest.raises(BadOAuth2Config):
            service.exchange_auth_code("http://example.com?state=state_value")

    def test_exchange_auth_code_raises_with_a_bad_jwt(self, service, jwt, _check_nonce):
        _check_nonce.return_value = True
        jwt.decode.side_effect = InvalidTokenError()

        with pytest.raises(UserNotAuthenticated):
            service.exchange_auth_code("http://example.com?state=state_value")

    def test_check_nonce(self, service, jwt):
        jwt.decode.side_effect = InvalidTokenError()

        assert service._check_nonce("something-wrong") is False

    @pytest.fixture
    def client_config(self):
        return {
            "client_id": sentinel.client_id,
            "client_secret": sentinel.client_secret,
            "redirect_uri": "http://example.com",
        }

    @pytest.fixture
    def service(self, client_config):
        return GoogleAuthService("secret", client_config)

    @pytest.fixture
    def flow(self, Flow):
        flow = Flow.from_client_config.return_value
        flow.authorization_url.return_value = sentinel.authorization_url, sentinel.state

        return flow

    @pytest.fixture(autouse=True)
    def os(self, patch):
        return patch("pyramid_googleauth.services.google_auth.os")

    @pytest.fixture(autouse=True)
    def jwt(self, patch):
        return patch("pyramid_googleauth.services.google_auth.jwt")

    @pytest.fixture(autouse=True)
    def json(self, patch):
        return patch("pyramid_googleauth.services.google_auth.json")

    @pytest.fixture
    def base64(self, patch):
        return patch("pyramid_googleauth.services.google_auth.base64")

    @pytest.fixture(autouse=True)
    def Flow(self, patch):
        return patch("pyramid_googleauth.services.google_auth.Flow")

    @pytest.fixture
    def _get_nonce(self, patch_object):
        patch = patch_object(GoogleAuthService, "_get_nonce")
        patch.return_value = "SOME-JWT"
        return patch

    @pytest.fixture
    def _check_nonce(self, patch_object):
        return patch_object(GoogleAuthService, "_check_nonce")

    @pytest.fixture
    def _decode_state(self, patch_object):
        return patch_object(GoogleAuthService, "_decode_state")


class TestFactory:
    def test_it(self, pyramid_request):
        pyramid_request.registry.settings = {
            "pyramid_googleauth.google_client_id": sentinel.google_client_id,
            "pyramid_googleauth.google_client_secret": sentinel.google_client_secret,
            "pyramid_googleauth.secret": "not_secret",
        }

        result = factory(sentinel.context, pyramid_request)

        assert result._client_id == sentinel.google_client_id
        assert result._client_secret == sentinel.google_client_secret
        assert result._redirect_uri == "http://example.com/googleauth/login/callback"
