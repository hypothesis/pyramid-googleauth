from pyramid.authentication import SessionAuthenticationHelper

DEFAULT_PERMISSION = "admin"


class GoogleSecurityPolicy:
    def __init__(self):
        self._session_authentication_helper = SessionAuthenticationHelper()

    def identity(self, request):
        raise NotImplementedError()

    def authenticated_userid(self, request):
        return self._session_authentication_helper.authenticated_userid(request)

    def permits(self, request, context, permission):
        raise NotImplementedError()

    def remember(self, request, userid, **kwargs):
        return self._session_authentication_helper.remember(request, userid, **kwargs)

    def forget(self, request, **kwargs):
        return self._session_authentication_helper.forget(request, **kwargs)
