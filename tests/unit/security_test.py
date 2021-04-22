from unittest.mock import sentinel

import pytest
from pyramid.security import Allowed, Denied


class TestGoogleSecurityPolicy:
    def test_session(self, policy):
        assert policy.session.userid_key == "googleauth.userid"

    @pytest.mark.parametrize(
        "userid,expected_identity",
        [
            ("testuser@hypothes.is", ["admin"]),
            ("testuser@example.com", []),
        ],
    )
    def test_identity(self, policy, pyramid_request, userid, expected_identity):
        pyramid_request.session["googleauth.userid"] = userid

        assert policy.identity(pyramid_request) == expected_identity

    def test_identity_when_no_user_is_logged_in(self, policy, pyramid_request):
        assert policy.identity(pyramid_request) == []

    def test_authenticated_userid(self, policy, pyramid_request):
        pyramid_request.session["googleauth.userid"] = "testuser@hypothes.is"

        assert policy.authenticated_userid(pyramid_request) == "testuser@hypothes.is"

    @pytest.mark.parametrize(
        "permission,expected_result",
        [
            ("admin", Allowed("allowed")),
            ("some-other-permission", Denied("denied")),
        ],
    )
    def test_permits(self, policy, pyramid_request, permission, expected_result):
        pyramid_request.session["googleauth.userid"] = "testuser@hypothes.is"

        assert (
            policy.permits(pyramid_request, sentinel.context, permission)
            == expected_result
        )

    def test_remember(self, policy, pyramid_request):
        assert policy.remember(pyramid_request, "testuser@hypothes.is") == []

    def test_forget(self, policy, pyramid_request):
        assert policy.forget(pyramid_request) == []
