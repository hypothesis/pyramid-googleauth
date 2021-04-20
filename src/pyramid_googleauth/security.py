from typing import List, NamedTuple

from pyramid.authentication import SessionAuthenticationHelper
from pyramid.security import Allowed, Denied

DEFAULT_PERMISSION = "admin"


class Identity(NamedTuple):
    userid: str
    permissions: List[str]


def _get_identity(userid):
    if userid and userid.endswith("@hypothes.is"):
        return Identity(userid, permissions=[DEFAULT_PERMISSION])

    return Identity("", [])


class GoogleSecurityPolicy:
    def __init__(self):
        self._session_authentication_helper = SessionAuthenticationHelper()

    def identity(self, request):
        userid = self.authenticated_userid(request)

        get_identity = request.registry.settings.get(
            "pyramid_googleauth.get_identity_callable", _get_identity
        )

        return get_identity(userid)

    def authenticated_userid(self, request):
        return self._session_authentication_helper.authenticated_userid(request)

    def permits(self, request, context, permission):
        return _permits(self, request, context, permission)

    def remember(self, request, userid, **kwargs):
        return self._session_authentication_helper.remember(request, userid, **kwargs)

    def forget(self, request, **kwargs):
        return self._session_authentication_helper.forget(request, **kwargs)


def _permits(policy, request, _context, permission):
    if permission in policy.identity(request).permissions:
        return Allowed("allowed")

    return Denied("denied")
