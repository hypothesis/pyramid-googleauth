from unittest.mock import sentinel

import pytest
from pyramid.security import Allowed, Denied

from pyramid_googleauth.security import (
    DEFAULT_PERMISSION,
    GoogleSecurityPolicy,
    Identity,
)


class TestGoogleSecurityPolicy:
    @pytest.mark.parametrize(
        "userid,expected_identity",
        [
            (
                "testuser@hypothes.is",
                Identity(
                    "testuser@hypothes.is",
                    [DEFAULT_PERMISSION],
                ),
            ),
            (
                "testuser@example.com",
                Identity(
                    "",
                    [],
                ),
            ),
        ],
    )
    def test_identity(self, policy, pyramid_request, userid, expected_identity):
        pyramid_request.session["auth.userid"] = userid

        assert policy.identity(pyramid_request) == expected_identity

    def test_identity_when_no_user_is_logged_in(self, policy, pyramid_request):
        assert policy.identity(pyramid_request) == Identity("", [])

    def test_authenticated_userid(self, policy, pyramid_request):
        pyramid_request.session["auth.userid"] = "testuser@hypothes.is"

        assert policy.authenticated_userid(pyramid_request) == "testuser@hypothes.is"

    @pytest.mark.parametrize(
        "permission,expected_result",
        [
            (DEFAULT_PERMISSION, Allowed("allowed")),
            ("some-other-permission", Denied("denied")),
        ],
    )
    def test_permits(self, policy, pyramid_request, permission, expected_result):
        pyramid_request.session["auth.userid"] = "testuser@hypothes.is"

        assert (
            policy.permits(pyramid_request, sentinel.context, permission)
            == expected_result
        )

    def test_remember(self, policy, pyramid_request):
        assert policy.remember(pyramid_request, "testuser@hypothes.is") == []

    def test_forget(self, policy, pyramid_request):
        assert policy.forget(pyramid_request) == []

    @pytest.fixture
    def policy(self):
        return GoogleSecurityPolicy()
