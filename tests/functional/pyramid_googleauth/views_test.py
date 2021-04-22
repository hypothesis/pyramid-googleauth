# pylint: disable=too-many-arguments
import logging

import pytest
from h_matchers import Any

from tests.functional.matchers import temporary_redirect_to


class TestLogin:
    def test_it_logs_the_user_in_and_redirects_to_google_login_page(
        self, app, route_url
    ):
        response = app.get("/googleauth/login")

        assert response == temporary_redirect_to(
            Any.url.matching("https://accounts.google.com/o/oauth2/v2/auth").with_query(
                dict(
                    response_type="code",
                    client_id="google_client_id",
                    redirect_uri=route_url("pyramid_googleauth.login.callback"),
                    scope=Any.string(),
                    state=Any.string(),
                    access_type="offline",
                    include_granted_scopes="true",
                    prompt="select_account",
                )
            )
        )


class TestLoginCallback:
    @pytest.mark.usefixtures("mock_google_auth_service")
    def test_it_redirects_to_success_redirect(self, app, nonce):
        response = app.get("/googleauth/login/callback", params={"state": nonce})

        assert response == temporary_redirect_to("https://localhost/protected")
        # Webtest handles cookies so if we follow the redirect to the admin
        # page we should be authenticated and get a 200 OK not a redirect to
        # the login page.
        response.follow(status=200)

    @pytest.mark.parametrize(
        "params,logged_text",
        [
            pytest.param(
                {
                    # An "error" param in the query string of the URL that Google calls us on.
                    "error": "foo"
                },
                "Error returned from authentication",
                id="An error from Google",
            ),
            pytest.param(
                {
                    # An invalid "state" param in the query string of the URL that Google calls
                    "state": "invalid"
                },
                "State check failed",
                id="State param is invalid",
            ),
            pytest.param(
                {},  # No "state" param in the query string of the URL that Google calls us on.
                "State check failed",
                id="State param missing",
                marks=pytest.mark.xfail(
                    raises=TypeError,
                    reason="Bug: it crashes if there's no 'state' in the request from Google",
                ),
            ),
        ],
    )
    def test_if_theres_a_problem_it_redirects_to_the_login_failure_page(
        self,
        app,
        caplog,
        route_url,
        params,
        logged_text,
    ):
        caplog.set_level(logging.WARNING)

        response = app.get("/googleauth/login/callback", params)

        assert logged_text in caplog.text
        assert response == temporary_redirect_to(
            route_url("pyramid_googleauth.login.failure")
        )

    @pytest.fixture
    def nonce(self, mock_google_auth_service):
        return mock_google_auth_service._get_nonce()  # pylint: disable=protected-access


class TestLogout:
    def test_if_youre_not_logged_in_it_redirects_you_to_the_login_page(
        self, app, route_url
    ):
        response = app.get("/googleauth/logout")

        assert response == temporary_redirect_to(route_url("pyramid_googleauth.login"))

    @pytest.mark.usefixtures("logged_in")
    def test_if_youre_logged_in_it_logs_you_out_cant_access_protected(
        self, app, route_url
    ):
        response = app.get("/googleauth/logout")

        assert response == temporary_redirect_to(
            route_url("pyramid_googleauth.login", _query={"hint": "user@hypothes.is"})
        )
        app.get("/protected", status=403)
