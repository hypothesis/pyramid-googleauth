from unittest import mock
from unittest.mock import sentinel

import pytest
from h_matchers import Any

from pyramid_googleauth.exceptions import UserNotAuthenticated
from pyramid_googleauth.services import GoogleAuthService
from pyramid_googleauth.views import login, login_callback, login_failure, logout


@pytest.mark.usefixtures("google_auth_service_factory")
class TestLogin:
    def test_it_redirects_to_google(self, pyramid_request, google_auth_service_factory):
        response = login(sentinel.context, pyramid_request)

        google_auth_service_factory.return_value.login_url.assert_called_once_with(
            force_login=True, login_hint=None, next_=None
        )
        assert (
            response.location
            == google_auth_service_factory.return_value.login_url.return_value
        )

    def test_it_allows_a_smooth_login_for_authenticated_users(
        self, pyramid_config, pyramid_request, google_auth_service_factory
    ):
        pyramid_config.testing_securitypolicy(userid="staff@hypothes.is")

        login(sentinel.context, pyramid_request)

        google_auth_service_factory.return_value.login_url.assert_called_once_with(
            force_login=False, login_hint="staff@hypothes.is", next_=None
        )

    def test_it_suggests_a_user_from_hint_parameter(
        self, pyramid_request, google_auth_service_factory
    ):
        pyramid_request.GET["hint"] = "staff@hypothes.is"

        login(sentinel.context, pyramid_request)

        google_auth_service_factory.return_value.login_url.assert_called_once_with(
            force_login=True, login_hint="staff@hypothes.is", next_=None
        )

    def test_it_propagates_the_next_parameter(
        self, pyramid_request, google_auth_service_factory
    ):
        pyramid_request.GET["next"] = sentinel.next

        login(sentinel.context, pyramid_request)

        google_auth_service_factory.return_value.login_url.assert_called_once_with(
            force_login=True, login_hint=None, next_=sentinel.next
        )


@pytest.mark.usefixtures("google_auth_service_factory")
class TestLoginCallback:
    def test_it_sets_up_the_session(
        self, pyramid_config, pyramid_request, google_auth_service_factory
    ):
        pyramid_config.testing_securitypolicy(
            remember_result=[("Remember-Header", "remember_value")]
        )
        pyramid_request.session["some_noise"] = "which_should_be_cleared_out"
        user = {"email": "staff@hypothes.is", "user_other": "user_value"}

        google_auth_service_factory.return_value.exchange_auth_code.return_value = (
            user,
            sentinel.credentials,
            {},
        )

        response = login_callback(sentinel.context, pyramid_request)

        assert pyramid_request.session == {"user": user}
        assert response.location == "/protected"
        assert "Remember-Header" in list(response.headers)

    def test_it_redirects_to_next(
        self, pyramid_config, pyramid_request, google_auth_service_factory
    ):
        pyramid_config.testing_securitypolicy(
            remember_result=[("Remember-Header", "remember_value")]
        )
        pyramid_request.session["some_noise"] = "which_should_be_cleared_out"

        google_auth_service_factory.return_value.exchange_auth_code.return_value = (
            {"email": "staff@hypothes.is", "user_other": "user_value"},
            sentinel.credentials,
            {"next": "/next"},
        )

        response = login_callback(sentinel.context, pyramid_request)

        assert response.location == "/next"

    def test_it_bails_out_if_the_user_is_not_authenticated(
        self, pyramid_request, google_auth_service_factory
    ):
        google_auth_service_factory.return_value.exchange_auth_code.side_effect = (
            UserNotAuthenticated
        )

        response = login_callback(sentinel.context, pyramid_request)

        assert response.location == "http://example.com/googleauth/login/failure"
        assert "Remember-Header" not in list(response.headers)


class TestLogout:
    def test_it_clears_the_session_and_redirects(self, pyramid_config, pyramid_request):
        pyramid_config.testing_securitypolicy(
            forget_result=[("Forget-Header", "forget_value")]
        )
        pyramid_request.session["some_noise"] = "which_should_be_cleared_out"

        response = logout(sentinel.context, pyramid_request)

        assert pyramid_request.session == {}
        assert response.location == "http://example.com/googleauth/login"
        assert "Forget-Header" in list(response.headers)

    def test_it_redirects_with_a_login_hint_if_possible(
        self, pyramid_config, pyramid_request
    ):
        pyramid_config.testing_securitypolicy(userid="staff@hypothes.is")

        response = logout(sentinel.context, pyramid_request)

        assert response.location == Any.url.containing_query(
            {"hint": "staff@hypothes.is"}
        )


class TestAdminLoginFailure:
    def test_it_returns_unauthorized(self, pyramid_request):
        response = login_failure(pyramid_request)

        assert not response
        assert pyramid_request.response.status_code == 401


@pytest.fixture
def google_auth_service_factory(patch):
    factory = patch("pyramid_googleauth.views.google_auth_service_factory")
    factory.return_value = mock.create_autospec(
        GoogleAuthService, spec_set=True, instance=True
    )
    return factory
